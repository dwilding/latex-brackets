[LaTeX Brackets][1] is a plugin for the [gedit][2] text editor that completes
common [LaTeX][3] brackets by automatically inserting the appropriate closing
bracket whenever a supported opening bracket is typed. It takes its inspiration
from the bracket completion plugin that is provided by the
[**`gedit-plugins`**][4] package.

To install the plugin in [GNOME][5] 2, move `latex-brackets.gedit-plugin` and
`latex-brackets.py` to the `~/.gnome2/gedit/plugins` directory. To install it in
GNOME 3, move `latex-brackets.plugin` and `latex-brackets.py` to the
`~/.local/share/gedit/plugins` directory. The plugin can then be enabled in
gedit's _Preferences_.

The supported opening brackets are

* `{`,
* `` ` ``,
* `$`,
* `\(`,
* `\[`

and all sizes (`\bigl`, `\Bigl`, `\biggl`, `\Biggl` and `\left`) of

* `(`
* `[`,
* `\{`,
* `\langle`,
* `\lbrace`,
* `\lceil`,
* `\lfloor`,
* `\lgroup`,
* `\lmoustache`,
* `\lvert`,
* `\lVert`.

Some of these brackets require the [**`amsmath`**][6] package.

LaTeX Brackets also provides some convenient keyboard features. If the cursor is
between a pair of opening and closing brackets then the backspace key removes
the whole pair. If the cursor is directly before a closing bracket then the
delete key removes the bracket and the tab key moves the cursor past the
bracket.

[1]: https://github.com/dwilding/latex-brackets
[2]: https://wiki.gnome.org/Apps/Gedit
[3]: http://www.latex-project.org/
[4]: https://wiki.gnome.org/Apps/Gedit/ShippedPlugins
[5]: http://www.gnome.org/
[6]: http://www.ctan.org/pkg/amsmath
