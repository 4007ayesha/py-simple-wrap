"""
easy_terminal is meant to make it easy to get styled output in the terminal.
Built on top of the rich library — no more memorizing markup strings.
"""


from __future__ import annotations


class EasyTerminal:
    """
    Builds styled terminal text by chaining style methods, then prints it.

    Nothing is printed until show() is called, so you can chain as many
    styles as you like first. Every set_* method returns the object itself,
    which is what makes the chaining work.

    Args:
        text (str): The text to print.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import EasyTerminal

            EasyTerminal("Hello World").set_color("red").set_bold().show()
            ```

        === "The Traditional Way"
            ```python
            from rich.console import Console

            console = Console()
            console.print("Hello World", style="bold red")
            ```
    """
    def __init__(self, text: str) -> None:
        self.text = text
        self.color = "#ffffff"
        self.bg_color = None
        self.color_scheme = None
        self.weight = None
        self.styles = {}
        self.style_chain = None


    def set_color(self, color: str) -> EasyTerminal:
        """
        Sets the text color and returns the object so you can keep chaining.

        Args:
            color (str): A color name ("red"), a hex code ("#ff0000"),
                or an rgb string ("rgb(255,0,0)").

        Returns:
            EasyTerminal: The same object, ready for the next call.

        Example:
            === "The Py_simple Way"
                ```python
                from py_simple import EasyTerminal

                EasyTerminal("Hello").set_color("#ff0000").show()
                ```

            === "The Traditional Way"
                ```python
                from rich.console import Console

                console = Console()
                console.print("Hello", style="#ff0000")
                ```
    """
        self.color = color
        return self


    def set_bg_color(self, color: str) -> EasyTerminal:
        """
        Sets the background color and returns the object for chaining.

        Args:
            color (str): A color name ("blue"), a hex code ("#0000ff"),
                or an rgb string ("rgb(0,0,255)").

        Returns:
            EasyTerminal: The same object, ready for the next call.

        Example:
            === "The Py_simple Way"
                ```python
                from py_simple import EasyTerminal

                EasyTerminal("Hello").set_color("white").set_bg_color("blue").show()
                ```

            === "The Traditional Way"
                ```python
                from rich.console import Console

                console = Console()
                console.print("Hello", style="white on blue")
                ```
        """
        self.bg_color = color
        return self


    def set_bold(self) -> EasyTerminal:
        """
        Makes the text bold and returns the object for chaining.

        Replaces any weight set earlier, so calling set_bold() after
        set_light_weight() leaves the text bold, not both.

        Returns:
            EasyTerminal: The same object, ready for the next call.

        Example:
            === "The Py_simple Way"
                ```python
                from py_simple import EasyTerminal

                EasyTerminal("Hello").set_bold().show()
                ```

            === "The Traditional Way"
                ```python
                from rich.console import Console

                console = Console()
                console.print("Hello", style="bold")
                ```
        """
        self.weight = "bold"
        self.styles['weight'] = self.weight
        return self


    def set_light_weight(self) -> EasyTerminal:
        """
        Makes the text dim (lighter than normal) and returns the object.

        Terminals only have bold, normal and dim, so this is the lightest
        weight available. It replaces any weight set earlier.

        Returns:
            EasyTerminal: The same object, ready for the next call.

        Example:
            === "The Py_simple Way"
                ```python
                from py_simple import EasyTerminal

                EasyTerminal("Hello").set_light_weight().show()
                ```

            === "The Traditional Way"
                ```python
                from rich.console import Console

                console = Console()
                console.print("Hello", style="dim")
                ```
        """
        self.weight = "dim"
        self.styles['weight'] = self.weight
        return self


    def _check_color_scheme(self) -> EasyTerminal:
        """Combines the text and background colors into one rich style."""
        if self.bg_color is not None:
            self.color_scheme = f"{self.color} on {self.bg_color}"
        else:
            self.color_scheme = self.color
        self.styles['color_scheme'] = self.color_scheme
        return self


    def _chain_styles(self) -> EasyTerminal:
        """Joins all chosen styles into a single space-separated string."""
        self._check_color_scheme()
        style_list = list(self.styles.values())
        style_list = [i for i in style_list if i is not None]
        self.style_chain = " ".join(style_list)
        return self


    def show(self) -> None:
        """
        Prints the text to the terminal with all the chosen styles.

        Call this last. Anything you didn't set falls back to the terminal's
        normal look (the text color defaults to white).

        Example:
            === "The Py_simple Way"
                ```python
                from py_simple import EasyTerminal

                EasyTerminal("Hello World").set_color("red").set_bg_color("white").set_bold().show()
                ```

            === "The Traditional Way"
                ```python
                from rich.console import Console

                console = Console()
                console.print("Hello World", style="bold red on white")
                ```
        """
        from rich.console import Console

        self._chain_styles()

        c = Console()
        c.print(self.text, style=self.style_chain)

