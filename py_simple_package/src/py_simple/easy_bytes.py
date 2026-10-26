"""
easy_bytes turns byte counts into readable sizes and back.
"""

import math
from decimal import MAX_EMAX, MIN_EMIN, Context, Decimal


class EasyBytesError(Exception):
    """
    Raised when a size cannot be converted.

    Args:
        message (str): Description of what went wrong.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


_KB_UNITS = ("B", "KB", "MB", "GB", "TB")  # KB-style names
_KIB_UNITS = ("B", "KiB", "MiB", "GiB", "TiB")  # KiB-style names (always 1024)

_UNITS = _KB_UNITS + _KIB_UNITS[1:]  # Every accepted unit name

# How many bytes are in each unit. KiB-style names always mean 1024. KB-style
# names mean 1024 by default (the original behavior) and 1000 when the caller
# asks for decimal units.
_KIB_MULTIPLIERS = {unit: 1024**power for power, unit in enumerate(_KIB_UNITS)}
_LEGACY_MULTIPLIERS = {
    **{unit: 1024**power for power, unit in enumerate(_KB_UNITS)},
    **_KIB_MULTIPLIERS,
}
_DECIMAL_MULTIPLIERS = {
    **{unit: 1000**power for power, unit in enumerate(_KB_UNITS)},
    **_KIB_MULTIPLIERS,
}


def _check_flag(name: str, value) -> None:
    """Raise `EasyBytesError` unless `value` is a real boolean."""
    if not isinstance(value, bool):
        raise EasyBytesError(
            f"\n\nERROR: {name} must be a boolean (True or False)."
        ) from None


def _scale_to_bytes(number_text: str, multiplier: int) -> int:
    """
    Multiply a numeric string by `multiplier` without float rounding loss.

    The product is computed exactly with `Decimal`, so `"1.001"` times 1000 is
    1001 and not 1000.9999999999999. Any real fractional byte is truncated.
    Raises `EasyBytesError` if `Decimal` cannot represent the number.
    """
    context = Context(
        prec=len(number_text) + len(str(multiplier)) + 2,
        Emax=MAX_EMAX,
        Emin=MIN_EMIN,
    )
    try:
        return int(context.multiply(Decimal(number_text), multiplier))
    except ArithmeticError:
        # Decimal cannot represent some extreme inputs, such as an exponent
        # with hundreds of digits, even though float() accepted them.
        raise EasyBytesError(
            "\n\nERROR: size could not be converted to a whole byte count."
        ) from None


def bytes_to_human(num_bytes: int, binary: bool = False, decimal: bool = False) -> str:
    """
    Turn a byte count into a short label such as `"1.5 KB"`.

    By default, `KB`, `MB`, `GB` and `TB` count in factors of 1024, as they
    always have. Use `binary=True` to get the same numbers spelled with `KiB`,
    `MiB`, `GiB` and `TiB`, or `decimal=True` to count in factors of 1000.

    Args:
        num_bytes (int): Number of bytes. Must be zero or greater.
        binary (bool): When `True`, label the size with `KiB`, `MiB`, `GiB` and
            `TiB` (1 KiB is 1024 bytes). Defaults to `False`.
        decimal (bool): When `True`, use decimal units where 1 KB is 1000
            bytes. Defaults to `False`, where 1 KB is 1024 bytes. Cannot be
            combined with `binary=True`.

    Returns:
        str: A size label using B, KB, MB, GB, or TB (or KiB, MiB, GiB, TiB
            when `binary` is `True`).

    Raises:
        EasyBytesError: If `num_bytes` is not a non-negative integer, if
            `binary` or `decimal` is not a boolean, or if both are `True`.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import bytes_to_human

            print(bytes_to_human(1536))
            print(bytes_to_human(1536, binary=True))
            print(bytes_to_human(1500, decimal=True))
            ```

        === "The Traditional Way"
            ```python
            size = 1536
            label = f"{size / 1024:.1f} KB" if size >= 1024 else f"{size} B"

            size = 1536
            label = f"{size / 1024:.1f} KiB" if size >= 1024 else f"{size} B"

            size = 1500
            label = f"{size / 1000:.1f} KB" if size >= 1000 else f"{size} B"
            ```
    """
    if isinstance(num_bytes, bool) or not isinstance(num_bytes, int) or num_bytes < 0:
        raise EasyBytesError(
            "\n\nERROR: num_bytes must be a non-negative integer."
        ) from None
    _check_flag("binary", binary)
    _check_flag("decimal", decimal)
    if binary and decimal:
        raise EasyBytesError(
            "\n\nERROR: binary and decimal cannot both be True."
        ) from None

    units = _KIB_UNITS if binary else _KB_UNITS
    base = 1000 if decimal else 1024

    size = float(num_bytes)
    unit = units[0]
    for name in units:
        unit = name
        if size < base or name == units[-1]:
            break
        size /= base

    if unit == "B":
        return f"{int(size)} B"
    rounded = round(size, 1)
    if rounded == int(rounded):
        return f"{int(rounded)} {unit}"
    return f"{rounded} {unit}"


def human_to_bytes(label: str, decimal: bool = False) -> int:
    """
    Turn a size label such as `"1.5 KB"` back into a byte count.

    By default, `KB`, `MB`, `GB` and `TB` count in factors of 1024, as they
    always have, so `"1 KB"` is 1024 bytes. `KiB`, `MiB`, `GiB` and `TiB`
    always count in factors of 1024. Pass `decimal=True` to make `KB`, `MB`,
    `GB` and `TB` count in factors of 1000 instead, so `"1 KB"` is 1000 bytes.
    A fractional byte is truncated.

    Args:
        label (str): A number plus a unit: B, KB, MB, GB, TB, KiB, MiB, GiB
            or TiB.
        decimal (bool): When `True`, `KB`-style units use factors of 1000.
            Defaults to `False`.

    Returns:
        int: The size in bytes.

    Raises:
        EasyBytesError: If `label` is not a recognized size, does not
            convert to a finite byte count, or if `decimal` is not a boolean.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import human_to_bytes

            print(human_to_bytes("1.5 KB"))
            print(human_to_bytes("1.5 KB", decimal=True))
            print(human_to_bytes("1.5 KiB"))
            ```

        === "The Traditional Way"
            ```python
            number, unit = "1.5 KB".split()
            print(int(float(number) * 1024))

            number, unit = "1.5 KB".split()
            print(int(float(number) * 1000))

            number, unit = "1.5 KiB".split()
            print(int(float(number) * 1024))
            ```
    """
    _check_flag("decimal", decimal)
    if not isinstance(label, str):
        raise EasyBytesError("\n\nERROR: label must be a string.") from None
    parts = label.strip().split()
    if len(parts) != 2:
        raise EasyBytesError("\n\nERROR: use a form like '1.5 KB'.") from None
    number_text, unit = parts
    multipliers = _DECIMAL_MULTIPLIERS if decimal else _LEGACY_MULTIPLIERS
    if unit not in multipliers:
        raise EasyBytesError(
            "\n\nERROR: unit must be B, KB, MB, GB, TB, KiB, MiB, GiB, or TiB."
        ) from None
    try:
        number = float(number_text)
    except ValueError as error:
        raise EasyBytesError(f"\n\nERROR: {error}") from None
    if number < 0:
        raise EasyBytesError("\n\nERROR: size cannot be negative.") from None
    multiplier = multipliers[unit]
    # The float is only used to validate the input (nan, inf, overflow). The
    # actual byte count is computed exactly below.
    if not math.isfinite(number * multiplier):
        raise EasyBytesError(
            "\n\nERROR: size must convert to a finite byte count."
        ) from None
    return _scale_to_bytes(number_text, multiplier)


def percent_used(used: int, total: int) -> float:
    """
    Report how much of a storage total is already used.

    Args:
        used (int): Bytes already used.
        total (int): Bytes available in total. Must be greater than 0.

    Returns:
        float: The used share as a percent, rounded to one decimal place.

    Raises:
        EasyBytesError: If the numbers are not valid byte counts, or if
            `total` is not positive.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import percent_used

            print(percent_used(250, 1000))
            ```

        === "The Traditional Way"
            ```python
            print(round(250 / 1000 * 100, 1))
            ```
    """
    for value in (used, total):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise EasyBytesError(
                "\n\nERROR: used and total must be non-negative integers."
            ) from None
    if total < 1:
        raise EasyBytesError("\n\nERROR: total must be at least 1.") from None
    return round(used / total * 100, 1)


def remaining_bytes(used: int, total: int) -> int:
    """
    Calculates how many bytes remain in a storage total.

    Args:
        used (int): Bytes already used. Must be a non-negative integer
            no greater than `total`.
        total (int): Total capacity in bytes. Must be a non-negative integer.

    Returns:
        int: Unused bytes, such as 750 for 250 used out of 1000.
            A zero-capacity or full storage total has zero remaining bytes.

    Raises:
        EasyBytesError: If either count is negative, is not an integer,
            is a boolean, or if `used` exceeds `total`.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import remaining_bytes

            print(remaining_bytes(250, 1000))
            ```

        === "The Traditional Way"
            ```python
            used = 250
            total = 1000
            print(total - used)
            ```
    """
    for value in (used, total):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise EasyBytesError(
                "\n\nERROR: used and total must be non-negative integers."
            ) from None
    if used > total:
        raise EasyBytesError("\n\nERROR: used cannot exceed total.") from None
    return total - used


def add_bytes(values: list, decimal: bool = False) -> int:
    """
    Add up a list of sizes and return the total in bytes.

    Each value is either an integer (already a byte count) or a size label
    such as `"1 KiB"` (1024 bytes). Labels such as `"1 KB"` follow the same
    rule as `human_to_bytes`: 1024 bytes by default, or 1000 bytes with
    `decimal=True`.

    Args:
        values (list): Byte counts (non-negative integers) and/or size
            labels. A tuple is accepted too. An empty list adds up to 0.
        decimal (bool): When `True`, `KB`-style units use factors of 1000.
            Defaults to `False`.

    Returns:
        int: The sum of all the values, in bytes.

    Raises:
        EasyBytesError: If `values` is not a list or a tuple, if an item is
            neither a non-negative integer nor a string, if a string is not
            a valid size label, or if `decimal` is not a boolean.
    """
    _check_flag("decimal", decimal)
    if not isinstance(values, (list, tuple)):
        raise EasyBytesError(
            "\n\nERROR: values must be a list or a tuple.") from None

    total = 0
    for value in values:
        if isinstance(value, str):
            total += human_to_bytes(value, decimal=decimal)
        elif isinstance(value, int) and not isinstance(value,
                                                       bool) and value >= 0:
            total += value
        else:
            raise EasyBytesError(
                "\n\nERROR: each value must be a non-negative integer or a size string."
            ) from None
    return total

def percent_free(used: int, total: int) -> float:
    """
    Report how much of a storage total is still free.

    Args:
        used (int): Bytes already used. Must be a non-negative integer
            no greater than `total`.
        total (int): Bytes available in total. Must be greater than 0.

    Returns:
        float: The free share as a percent, rounded to one decimal place.

    Raises:
        EasyBytesError: If the numbers are not valid byte counts, if
            `total` is not positive, or if `used` exceeds `total`.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import percent_free

            print(percent_free(250, 1000))
            ```

        === "The Traditional Way"
            ```python
            used = 250
            total = 1000
            print(round((total - used) / total * 100, 1))
            ```
    """
    for value in (used, total):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise EasyBytesError(
                "\n\nERROR: used and total must be non-negative integers."
            ) from None
    if total < 1:
        raise EasyBytesError("\n\nERROR: total must be at least 1.") from None
    if used > total:
        raise EasyBytesError("\n\nERROR: used cannot exceed total.") from None
    return round((total - used) / total * 100, 1)

