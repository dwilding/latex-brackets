# This is latex-brackets.py, a bracket completion plugin for the gedit text
# editor. See <https://github.com/dwilding/latex-brackets>.
#
# Copyright (c) 2012 Dave Wilding
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from gi.repository import GObject, Gedit, Gdk


def sizes(opening, closing):
	brackets = []

	for stub in ('\\Bigg', '\\bigg', '\\Big', '\\big'):
		brackets.append(('l'.join((stub, opening)), 'r'.join((stub, closing))))

	brackets.append(('\\left%s' % opening, '\\right%s' % closing))
	brackets.append((opening, closing))
	return brackets


def lr(name):
	return sizes('\\l%s' % name, '\\r%s' % name)


brackets = {Gdk.KEY_dollar: [('$', '$')],
            Gdk.KEY_quoteleft: [('`', '\'')],
            Gdk.KEY_parenleft: sizes('(', ')') + [('\\(', '\\)')],
            Gdk.KEY_bracketleft: sizes('[', ']') + [('\\[', '\\]')],
            Gdk.KEY_braceleft: [('{', '}')] + sizes('\\{', '\\}'),
            Gdk.KEY_e: lr('angle') + lr('brace') + lr('moustache'),
            Gdk.KEY_l: lr('ceil'),
            Gdk.KEY_p: lr('group'),
            Gdk.KEY_r: lr('floor'),
            Gdk.KEY_t: lr('vert') + lr('Vert')}


class LatexBracketsPlugin(GObject.Object, Gedit.ViewActivatable):
	__gtype_name__ = 'LatexBracketsPlugin'
	view = GObject.property(type=Gedit.View)

	def __init__(self):
		GObject.Object.__init__(self)

	def do_activate(self):
		self.text = self.view.get_buffer()
		self.live = False
		self.update_live()
		self.edit_handler = self.view.connect('notify::editable', self.update_live)
		self.lang_handler = self.text.connect('notify::language', self.update_live)

	def do_deactivate(self):
		self.view.disconnect(self.edit_handler)
		self.text.disconnect(self.lang_handler)

		if self.live:
			self.view.disconnect(self.after_handler)
			self.view.disconnect(self.press_handler)

	def update_live(self, view = None, pspec = None):
		"""Handle events if and only if the document is editable and has LaTeX highlighting."""
		edit = self.view.get_editable()
		lang = self.text.get_language()

		if edit and lang and lang.get_id() == 'latex':
			if not self.live:
				self.after_handler = self.view.connect('event-after', self.event_after)
				self.press_handler = self.view.connect('key-press-event', self.event_press)
				self.live = True

		elif self.live:
			self.live = False
			self.view.disconnect(self.after_handler)
			self.view.disconnect(self.press_handler)

	def event_after(self, view, event):
		ignore = Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD1_MASK

		if (event.type != Gdk.EventType.KEY_PRESS or
		    event.state & ignore or
		    event.keyval not in brackets):
			return

		insert = self.get_insert()
		closing = self.look_backward(insert, event.keyval)

		if closing:
			self.text.begin_user_action()
			self.text.insert(insert, closing)
			self.text.end_user_action()
			insert.backward_chars(len(closing))
			self.text.place_cursor(insert)

	def event_press(self, view, event):
		ignore = (Gdk.ModifierType.CONTROL_MASK |
		          Gdk.ModifierType.MOD1_MASK |
		          Gdk.ModifierType.SHIFT_MASK)

		if event.state & ignore or self.text.get_selection_bounds():
			return

		insert = self.get_insert()

		# Deal with the backspace key.
		if event.keyval == Gdk.KEY_BackSpace:
			bounds = self.look_both(insert)

			if bounds:
				self.text.begin_user_action()
				self.text.delete(*bounds)
				self.text.end_user_action()
				return True

		# Deal with the delete key(s).
		elif event.keyval in (Gdk.KEY_Delete, Gdk.KEY_KP_Delete):
			end = self.look_forward(insert)

			if end:
				self.text.begin_user_action()
				self.text.delete(insert, end)
				self.text.end_user_action()
				return True

		# Deal with the tab key(s).
		elif event.keyval in (Gdk.KEY_Tab, Gdk.KEY_KP_Tab):
			line = self.get_line(insert)

			# The tab key should function normally at the beginning of a line.
			if not line or line.isspace():
				return

			end = self.look_forward(insert)

			if end:
				self.text.place_cursor(end)
				return True

	def look_backward(self, end, key):
		"""If end follows an opening bracket return the corresponding closing bracket."""
		for (opening, closing) in brackets[key]:
			start = end.copy()
			start.backward_chars(len(opening))

			if start.get_text(end) == opening and not self.escaped(start):
				return closing

	def look_both(self, middle):
		"""If middle is between a pair of brackets return the TextIters surrounding that pair."""
		for key in brackets:
			for (opening, closing) in brackets[key]:
				start = middle.copy()
				start.backward_chars(len(opening))
				end = middle.copy()
				end.forward_chars(len(closing))

				if (start.get_text(middle) == opening and
				    not self.escaped(start) and
				    middle.get_text(end) == closing):
					return (start, end)

	def look_forward(self, start):
		"""If start preceeds a closing bracket return the TextIter following that bracket."""
		for key in brackets:
			for (opening, closing) in brackets[key]:
				end = start.copy()
				end.forward_chars(len(closing))

				if start.get_text(end) == closing:
					return end

	def escaped(self, end):
		"""Determine whether end is escaped by a backslash."""
		slashes = 0
		line = self.get_line(end)

		for char in reversed(line):
			if char == '\\':
				slashes += 1

			else:
				break

		return bool(slashes % 2)

	def get_line(self, end):
		"""Return the contents of the line to end."""
		line = end.get_line()
		start = self.text.get_iter_at_line(line)
		return start.get_text(end)

	def get_insert(self):
		"""Return the TextIter at the insertion point."""
		mark = self.text.get_insert()
		return self.text.get_iter_at_mark(mark)
