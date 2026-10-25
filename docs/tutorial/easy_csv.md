# Easy CSV

Working with CSV files is common when storing or exchanging structured data. Whether you're reading information, creating CSV files, checking columns, or filtering rows, `easy_csv` provides simple helpers that make working with CSV data easy to read and understand.

## A small real-world example

Imagine you're managing a list of people stored in a CSV file. You want to read the data, check which columns are available, and find a specific person without writing the CSV parsing logic yourself.

```python
from py_simple import read_csv_to_list, get_csv_columns, filter_csv_rows

columns = get_csv_columns("people.csv")
print(columns)

people = read_csv_to_list("people.csv")
print(people)

alice = filter_csv_rows(
    filepath="people.csv",
    column="Name",
    value="Alice",
)
print(alice)
```

Example output:

```text
['Name', 'Age']
[{'Name': 'Alice', 'Age': '24'}, {'Name': 'Bob', 'Age': '31'}]
[{'Name': 'Alice', 'Age': '24'}]
```

## What happened?

`get_csv_columns()` retrieves the column names from the first row of the CSV file.

`read_csv_to_list()` reads the CSV file and returns its contents as a list of dictionaries by default. You can also set `return_dict=False` to receive the rows as lists.

`filter_csv_rows()` finds rows where a specific column matches the value you provide.

You can also use `write_csv_from_list()` to create a CSV file from a list of dictionaries or lists.

```python
from py_simple import write_csv_from_list

people = [
    {"Name": "Alice", "Age": "24"},
    {"Name": "Bob", "Age": "31"},
]

write_csv_from_list("people.csv", people)
```

## Combine files with matching headers

Use `merge_csv_files()` to join CSV files without loading them all into memory:

```python
from py_simple import merge_csv_files, write_csv_from_list, read_csv_to_list

write_csv_from_list("january.csv", [{"Name": "Alice", "Age": "24"}])
write_csv_from_list("february.csv", [{"Name": "Bob", "Age": "31"}])
merge_csv_files(["january.csv", "february.csv"], "combined.csv")
print(read_csv_to_list("combined.csv"))
# [{'Name': 'Alice', 'Age': '24'}, {'Name': 'Bob', 'Age': '31'}]
```

Files are read as UTF-8, in the order supplied. The header appears once and
must match exactly, including column order. Quoted commas, embedded newlines,
Unicode, empty fields and data record field counts are preserved. Use
`delimiter=";"` if all the files use semicolons.

Header-only files are accepted. An empty input list, a zero-byte file or a
blank first record raises `ValueError`, as do mismatched headers. Invalid
CSV quoting raises `csv.Error`; file and decoding errors propagate.

Choose an output path different from every input, including symbolic and hard
links. Its parent directory must already exist. The helper uses a temporary
file there and replaces the destination only after every input succeeds.
Inputs and an existing destination remain unchanged if merging fails.
An unrelated output symlink is replaced, leaving its target unchanged;
file permissions and other metadata are not copied to the new output.

## Why use these helpers?

Instead of repeatedly opening files, creating CSV readers and writers, handling headers, and filtering rows manually, you can simply write:

```python
people = read_csv_to_list("people.csv")

alice = filter_csv_rows(
    "people.csv",
    column="Name",
    value="Alice",
)
```

These helpers keep working with CSV files simple, readable, and beginner-friendly while making common tasks such as reading, writing, inspecting, and filtering CSV data easier.
