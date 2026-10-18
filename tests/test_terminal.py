from py_simple_package.src.py_simple.easy_terminal import EasyTerminal


def test_init_default_color():
    terminal = EasyTerminal("Hello")
    assert terminal.color == "#ffffff"


def test_init_defaults():
    terminal = EasyTerminal("Hello")
    assert terminal.bg_color is None
    assert terminal.color_scheme is None
    assert terminal.weight is None
    assert terminal.styles == {}
    assert terminal.style_chain is None


def test_set_color():
    terminal = EasyTerminal("Hello")
    colors = [
        "red", "blue", "green", "yellow",
        "#bee6c9", "#99238d", "#1c0219", "#454138",
    ]
    for color in colors:
        result = terminal.set_color(color)
        assert terminal.color == color
        assert result is terminal


def test_set_bg_color():
    terminal = EasyTerminal("Hello")
    colors = [
        "red", "blue", "green", "yellow",
        "#bee6c9", "#99238d", "#1c0219", "#454138",
    ]
    for color in colors:
        result = terminal.set_bg_color(color)
        assert terminal.bg_color == color
        assert result is terminal


def test_set_bold():
    terminal = EasyTerminal("Hello")
    result = terminal.set_bold()
    assert terminal.weight == "bold"
    assert terminal.styles["weight"] == "bold"
    assert result is terminal


def test_set_light_weight():
    terminal = EasyTerminal("Hello")
    result = terminal.set_light_weight()
    assert terminal.weight == "dim"
    assert terminal.styles["weight"] == "dim"
    assert result is terminal


def test_weight_replaces_previous():
    terminal = EasyTerminal("Hello")
    terminal.set_bold()
    terminal.set_light_weight()
    assert terminal.weight == "dim"
    assert terminal.styles["weight"] == "dim"


def test_check_color_scheme_without_bg():
    terminal = EasyTerminal("Hello")
    terminal.set_color("red")
    terminal._check_color_scheme()
    assert terminal.color_scheme == "red"


def test_check_color_scheme_with_bg():
    terminal = EasyTerminal("Hello")
    terminal.set_color("red")
    terminal.set_bg_color("blue")
    terminal._check_color_scheme()
    assert terminal.color_scheme == "red on blue"


def test_chain_styles_combines_everything():
    terminal = EasyTerminal("Hello")
    terminal.set_color("red")
    terminal.set_bg_color("blue")
    terminal.set_bold()
    terminal._chain_styles()
    assert terminal.style_chain == "bold red on blue"


def test_show_prints_text(capsys):
    terminal = EasyTerminal("Hello World")
    terminal.show()
    captured = capsys.readouterr()
    assert captured.out == "Hello World\n"


def test_show_with_styles_still_prints_text(capsys):
    terminal = EasyTerminal("Hello World").set_color("red").set_bg_color("blue").set_bold()
    terminal.show()
    captured = capsys.readouterr()
    assert captured.out == "Hello World\n"
