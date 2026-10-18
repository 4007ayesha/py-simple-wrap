import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest

from py_simple_package.src.py_simple import plot_bar_chart as public_plot_bar_chart
from py_simple_package.src.py_simple.easy_data_visualization import plot_bar_chart


@pytest.fixture(autouse=True)
def mock_plt_show(monkeypatch):
    """Prevent matplotlib from popping up windows during tests."""
    monkeypatch.setattr(plt, "show", lambda: None)
    yield
    plt.close("all")


def test_plot_bar_chart_draws_one_bar_per_value():
    plot_bar_chart(["Mon", "Tue", "Wed"], [3.5, 2.0, 4.5])
    ax = plt.gca()
    assert len(ax.patches) == 3


def test_plot_bar_chart_bar_heights_match_values():
    plot_bar_chart(["A", "B", "C"], [1, 5, 3])
    heights = [bar.get_height() for bar in plt.gca().patches]
    assert heights == [1, 5, 3]


def test_plot_bar_chart_sets_title_and_axis_labels():
    plot_bar_chart(
        ["Mon", "Tue"],
        [3.5, 2.0],
        title="My Screen Time",
        x_label="Day",
        y_label="Hours",
    )
    ax = plt.gca()
    assert ax.get_title() == "My Screen Time"
    assert ax.get_xlabel() == "Day"
    assert ax.get_ylabel() == "Hours"


def test_plot_bar_chart_without_title_or_labels_leaves_them_blank():
    plot_bar_chart(["A", "B"], [1, 2])
    ax = plt.gca()
    assert ax.get_title() == ""
    assert ax.get_xlabel() == ""
    assert ax.get_ylabel() == ""


def test_plot_bar_chart_uses_labels_on_x_axis():
    plot_bar_chart(["Mon", "Tue", "Wed"], [1, 2, 3])
    fig = plt.gcf()
    fig.canvas.draw()
    tick_text = [t.get_text() for t in plt.gca().get_xticklabels()]
    assert tick_text == ["Mon", "Tue", "Wed"]


def test_plot_bar_chart_accepts_numeric_labels():
    plot_bar_chart([2024, 2025, 2026], [10, 20, 30])
    assert len(plt.gca().patches) == 3


def test_plot_bar_chart_empty_labels_raises_value_error():
    with pytest.raises(ValueError, match="cannot be empty"):
        plot_bar_chart([], [1, 2])


def test_plot_bar_chart_empty_values_raises_value_error():
    with pytest.raises(ValueError, match="cannot be empty"):
        plot_bar_chart(["A", "B"], [])


def test_plot_bar_chart_mismatched_lengths_raises_value_error():
    with pytest.raises(ValueError, match="same length"):
        plot_bar_chart(["A", "B", "C"], [1, 2])


def test_plot_bar_chart_non_numeric_value_raises_value_error():
    with pytest.raises(ValueError, match="must be numbers"):
        plot_bar_chart(["A", "B"], [1, "two"])


def test_plot_bar_chart_boolean_value_raises_value_error():
    with pytest.raises(ValueError, match="must be numbers"):
        plot_bar_chart(["A", "B"], [1, True])


def test_plot_bar_chart_is_available_from_public_api():
    assert public_plot_bar_chart is plot_bar_chart
