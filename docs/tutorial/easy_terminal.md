# Easy Terminal

Styling terminal output can make important messages easier to notice. `easy_terminal` provides a simple way to add colors and text styles without having to work directly with Rich style strings.

## A small real-world example

Imagine you're running a build script and want successful builds to stand out clearly in the terminal.

```python
from py_simple import EasyTerminal
EasyTerminal("Build complete").set_color("green").set_bold().show()

```

Example output:

```text
Build complete
```

## What happened?

`EasyTerminal()` creates a terminal message that can be styled before it is printed.

`set_color("green")` changes the text color to green.

`set_bold()` makes the message bold.

Finally, `show()` prints the styled message to the terminal.

You can also use `set_bg_color()` to add a background color or `set_light_weight()` when you want dimmer text.

## Why use these helpers?

Without `EasyTerminal`, you would need to create a Rich console and manually build style strings such as `"bold green"`.

With `EasyTerminal`, the same styling can be expressed by chaining readable methods together, which keeps terminal output code simple and beginner-friendly.
