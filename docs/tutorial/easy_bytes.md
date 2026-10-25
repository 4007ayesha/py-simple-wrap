# Easy Bytes

File sizes arrive as large numbers of bytes. `1536` is harder to read than
`1.5 KB`, and the other direction matters when a form asks you to type a
size. `easy_bytes` converts both ways, adds sizes together, and can tell you
what percent of a drive is full or how many bytes remain.

## Which units mean what

By default, `KB`, `MB`, `GB` and `TB` count in factors of 1024. This is how
`easy_bytes` has always worked, so existing code keeps returning the same
numbers. The `KiB`, `MiB`, `GiB` and `TiB` units are also accepted, and they
mean exactly the same thing as the default `KB`-style units.

If you need `KB` to mean 1000 bytes (the way drive makers and many websites
count), pass `decimal=True`.

| Unit  | Default           | With `decimal=True` |
| ----- | ----------------- | ------------------- |
| `B`   | 1                 | 1                   |
| `KB`  | 1,024             | 1,000               |
| `MB`  | 1,048,576         | 1,000,000           |
| `GB`  | 1,073,741,824     | 1,000,000,000       |
| `TB`  | 1,099,511,627,776 | 1,000,000,000,000   |
| `KiB` | 1,024             | 1,024               |
| `MiB` | 1,048,576         | 1,048,576           |
| `GiB` | 1,073,741,824     | 1,073,741,824       |
| `TiB` | 1,099,511,627,776 | 1,099,511,627,776   |

Units are case-sensitive: `"1 kb"` and `"1 kib"` are rejected.

## A small real-world example

Imagine a homework folder that can hold 10 MB, and the files inside already
use 2.5 MB.

```python
from py_simple import bytes_to_human, human_to_bytes, percent_used, remaining_bytes

used = human_to_bytes("2.5 MB")
total = human_to_bytes("10 MB")

print(bytes_to_human(used))
print(percent_used(used, total))
print(bytes_to_human(remaining_bytes(used, total)))
```

Example output:

```text
2.5 MB
25.0
7.5 MB
```

## Adding sizes together

`add_bytes()` takes a list that mixes plain byte counts and size labels, and
returns the total in bytes.

```python
from py_simple import add_bytes, bytes_to_human

total = add_bytes([512, "1 KB", "1 KiB"])

print(total)
print(bytes_to_human(total))
```

Example output:

```text
2560
2.5 KB
```

Here `512` is already a byte count, and `"1 KB"` and `"1 KiB"` are both 1024 bytes, 
in order to preserve beckwards compatibility. To count `"1 KB"` as 1000 bytes, pass `decimal=True`. 
The `decimal=True` parameter only works with values such as `KB, MB, GB and TB`. 
`KiB, MiB, GiB and TiB` are binary by default, so the `decimal=True` parameter doesn't affect them.
Here's an example:

```python
from py_simple import add_bytes

print(add_bytes([512, "1 KB", "1 KiB"], decimal=True))
```

```text
2536
```

## What happened?

`human_to_bytes()` reads a label like `"2.5 MB"` and returns the byte count.
The scaling is exact, so `"1.001 KB"` is `1001` bytes with `decimal=True`. 
A real fractional byte is cut off, so `"0.1 KiB"` becomes `102`.

`bytes_to_human()` turns a count back into a short label. Whole numbers drop
the decimal, so `2048` bytes becomes `"2 KB"`. It has two optional switches:

```python
from py_simple import bytes_to_human

print(bytes_to_human(1536))
print(bytes_to_human(1536, binary=True))
print(bytes_to_human(1500, decimal=True))
```

```text
1.5 KB
1.5 KiB
1.5 KB
```

`binary=True` writes the same numbers with `KiB`, `MiB`, `GiB` and `TiB`.
`decimal=True` counts in thousands instead. The two cannot be combined.

`add_bytes()` converts each string with `human_to_bytes()` first, then adds
everything up. Each item must be a non-negative whole number or a valid size
label, and the input must be a list or a tuple. An empty list adds up to `0`.

`percent_used()` compares the two counts and returns the filled share rounded
to one decimal place.

`remaining_bytes()` subtracts used bytes from the total. It accepts whole,
non-negative byte counts, including a total of zero when usage is also zero.
Booleans and usage greater than the total raise `EasyBytesError` instead of
returning a misleading count. A full storage total returns zero.

## Why use these helpers?

Mixing up 1000 and 1024 is easy once the unit climbs from KB to MB to GB.
These functions keep the unit list in one place, let you choose which one you
mean, and reject a negative size, a unit they do not know, or an item that is
not a number or a size label.
