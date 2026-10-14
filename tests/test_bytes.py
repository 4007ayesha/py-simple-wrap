import pytest

from py_simple_package.src.py_simple.easy_bytes import (
    EasyBytesError,
    bytes_to_human,
    human_to_bytes,
    percent_used,
)


@pytest.mark.parametrize(
    "num_bytes, expected",
    [
        (0, "0 B"),
        (1, "1 B"),
        (1023, "1023 B"),
        (1024, "1 KB"),
        (1025, "1 KB"),
        (1536, "1.5 KB"),
        (1587, "1.5 KB"),
        (1588, "1.6 KB"),
        (2047, "2 KB"),
        (2048, "2 KB"),
        (1023 * 1024, "1023 KB"),
        (1024**2, "1 MB"),
        (1023 * 1024**2, "1023 MB"),
        (1024**3, "1 GB"),
        (1023 * 1024**3, "1023 GB"),
        (1024**4, "1 TB"),
        (1536 * 1024**3, "1.5 TB"),
        (1024**5, "1024 TB"),
    ],
)
def test_bytes_to_human(num_bytes, expected):
    """Use binary units, one decimal place, and no unnecessary decimal zero."""
    assert bytes_to_human(num_bytes) == expected


@pytest.mark.parametrize("num_bytes", [-1, True, False, 1.0, 1.5, "1024", None, [], {}])
def test_bytes_to_human_rejects_bad_input(num_bytes):
    """Byte counts must be non-negative integers, excluding booleans."""
    with pytest.raises(
        EasyBytesError, match="num_bytes must be a non-negative integer"
    ):
        bytes_to_human(num_bytes)


@pytest.mark.parametrize(
    "label, expected",
    [
        ("0 B", 0),
        ("1 B", 1),
        ("512 B", 512),
        ("1.5 B", 1),
        ("0.1 KB", 102),
        ("1.5 KB", 1536),
        ("2 KB", 2048),
        ("1 MB", 1048576),
        ("1.5 MB", 1572864),
        ("1 GB", 1073741824),
        ("1.5 GB", 1610612736),
        ("1 TB", 1099511627776),
        ("1.5 TB", 1649267441664),
        ("0 TB", 0),
        ("  1.5 KB  ", 1536),
        ("\t1.5\t KB\n", 1536),
        ("1267650600228229401496703205376 B", 2**100),
        ("1267650600228229401496703205376 TB", 2**140),
        (f"{2**1023} B", 2**1023),
    ],
)
def test_human_to_bytes(label, expected):
    """Read supported units and whitespace, returning a whole byte count."""
    result = human_to_bytes(label)
    assert result == expected
    assert isinstance(result, int)


@pytest.mark.parametrize("label", [None, 1024, 1.5, True, False, [], {}])
def test_human_to_bytes_rejects_non_string(label):
    """Reject non-string labels with the module's exception."""
    with pytest.raises(EasyBytesError, match="label must be a string"):
        human_to_bytes(label)


@pytest.mark.parametrize(
    "label", ["", "  ", "lots", "1.5", "KB", "1.5KB", "1 KB extra"]
)
def test_human_to_bytes_rejects_bad_label(label):
    """A label must contain a number and a separate unit."""
    with pytest.raises(EasyBytesError, match="use a form like '1.5 KB'"):
        human_to_bytes(label)


@pytest.mark.parametrize("label", ["5 XB", "1 kb", "1 mb", "1 KiB"])
def test_human_to_bytes_rejects_unknown_unit(label):
    """Only the documented uppercase units are supported."""
    with pytest.raises(EasyBytesError, match="unit must be B, KB, MB, GB, or TB"):
        human_to_bytes(label)


@pytest.mark.parametrize("label", ["many KB", "1.2.3 MB", "--1 B"])
def test_human_to_bytes_rejects_malformed_number(label):
    """Invalid numeric text should be wrapped in EasyBytesError."""
    with pytest.raises(EasyBytesError, match="could not convert string to float"):
        human_to_bytes(label)


@pytest.mark.parametrize(
    "label", ["-1 B", "-0.5 KB", "-inf KB", "-Infinity TB", "-1e309 MB"]
)
def test_human_to_bytes_rejects_negative_size(label):
    """Reject negative sizes, including fractional ones."""
    with pytest.raises(EasyBytesError, match="size cannot be negative"):
        human_to_bytes(label)


@pytest.mark.parametrize(
    "label",
    [
        "nan KB",
        "NaN B",
        "+nan MB",
        "-NaN GB",
        "inf KB",
        "+inf B",
        "Infinity MB",
        "+INFINITY GB",
        "1e309 KB",
        "1e309 TB",
        "  NaN\tKB\n",
    ],
)
def test_human_to_bytes_rejects_nonfinite_size(label):
    """Non-finite numeric labels must use the public conversion error."""
    with pytest.raises(
        EasyBytesError, match="size must convert to a finite byte count"
    ):
        human_to_bytes(label)


@pytest.mark.parametrize("unit", ["KB", "MB", "GB", "TB"])
def test_human_to_bytes_rejects_scaled_overflow(unit):
    """A finite number can still overflow when scaled to bytes."""
    with pytest.raises(
        EasyBytesError, match="size must convert to a finite byte count"
    ):
        human_to_bytes(f"1e308 {unit}")


@pytest.mark.parametrize(
    "used, total, expected",
    [
        (0, 1000, 0.0),
        (0, 1, 0.0),
        (1, 1, 100.0),
        (1000, 1000, 100.0),
        (250, 1000, 25.0),
        (1, 3, 33.3),
        (2, 3, 66.7),
        (1, 8, 12.5),
        (1500, 1000, 150.0),
    ],
)
def test_percent_used(used, total, expected):
    """Return the used share as a float rounded to one decimal place."""
    result = percent_used(used, total)
    assert result == expected
    assert isinstance(result, float)


@pytest.mark.parametrize("invalid", [-1, True, False, 1.0, 1.5, "1", None, [], {}])
@pytest.mark.parametrize("argument", ["used", "total"])
def test_percent_used_rejects_bad_input(invalid, argument):
    """Validate each byte count independently, excluding booleans."""
    counts = {"used": 1, "total": 100}
    counts[argument] = invalid
    with pytest.raises(
        EasyBytesError, match="used and total must be non-negative integers"
    ):
        percent_used(**counts)


@pytest.mark.parametrize("used", [0, 1])
def test_percent_used_rejects_zero_total(used):
    """Even zero used bytes require a positive total."""
    with pytest.raises(EasyBytesError, match="total must be at least 1"):
        percent_used(used, 0)
