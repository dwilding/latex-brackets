[LaTeX Brackets][1] is a plugin for the [gedit][2] text editor that completes
common [LaTeX][3] brackets by automatically inserting the appropriate closing
bracket whenever a supported opening bracket is typed. It takes its inspiration
from the bracket completion plugin that is provided by the
[**`gedit-plugins`**][4] package.

To install the plugin simply copy `latex-brackets.plugin` and
`latex-brackets.py` to the `~/.local/share/gedit/plugins` directory (GNOME 3)
and then enable it in gedit's _Preferences_. The supported opening brackets are

* `{`,
* `` ` ``,
* `$`,
* `\(`,
* `\[`

and all sizes (`\bigl`, `\Bigl`, `\biggl`, `\Biggl` and `\left`) of

* `(`
* `[`,
* `\\{`,
* `\langle`,
* `\lbrace`,
* `\lmoustache`,
* `\lceil`,
* `\lgroup`,
* `\lfloor`,
* `\lvert`,
* `\lVert`.

Some of these brackets are provided by the [**`amsmath`**][5] package.

[1]: https://github.com/dwilding/latex-brackets
[2]: http://projects.gnome.org/gedit/
[3]: http://www.latex-project.org/
[4]: https://live.gnome.org/GeditPlugins
[5]: http://www.ctan.org/pkg/amsmath
