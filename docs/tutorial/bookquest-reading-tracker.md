# BookQuest: Build a Monthly Reading Tracker

In this tutorial, you'll build BookQuest, a simple Python application that helps you maintain a reading list, set a monthly reading goal, and review your reading progress over time.

You'll combine several `py_simple` modules:

- **Easy JSON** to save your books and monthly goal.
- **Easy Date Formatter** to display today's date.
- **Easy Stats** to analyze your monthly reading activity.
- **Easy Data Visualization** to visualize books completed per month.

## What you'll build

BookQuest lets you add books, record their start and finish dates, set a monthly target, and view a summary of your reading habits.

A book counts as completed in the month its finish date is recorded. A book still in progress is not counted as completed.

## Step 1: Import the helpers

Create a Python file named `bookquest.py` and import the required helpers:

```python
from datetime import date

from py_simple import (
    save_json_data,
    open_json,
    update_json,
    is_json_file,
    get_pretty_date,
    median,
    standard_deviation,
    data_range,
)
```

Python's built-in `date` class records the start and finish dates. The `py_simple` helpers handle JSON storage, readable dates, and statistics.

## Step 2: Store your reading data

We need to remember the reading list and monthly goal between program runs.

```python
DATA_FILE = "books.json"


def load_data():
    if is_json_file(DATA_FILE):
        data = open_json(DATA_FILE)
        data.setdefault("monthly_goal", 4)
        data.setdefault("books", [])
        return data

    data = {
        "monthly_goal": 4,
        "books": [],
    }
    save_json_data(DATA_FILE, data)
    return data


def save_data(data):
    if is_json_file(DATA_FILE):
        update_json(DATA_FILE, data)
    else:
        save_json_data(DATA_FILE, data)
```

`load_data()` opens the existing JSON file or creates a new reading tracker. `save_data()` persists changes to the file.

## Step 3: Add a book

Each book has a title, an optional author, a start date, a finish date, and a status.

```python
def add_book(data):
    title = input("Enter book title: ").strip()

    if not title:
        print("Book title cannot be empty.")
        return

    author = input("Enter author (optional): ").strip()

    book = {
        "title": title,
        "author": author,
        "start_date": date.today().isoformat(),
        "finish_date": None,
        "status": "reading",
    }

    data["books"].append(book)
    save_data(data)
```

The start date is recorded when the book is added. Its finish date remains `None` until you complete it.

## Step 4: Complete a book

When you finish reading, record the date and update the status:

```python
book["finish_date"] = date.today().isoformat()
book["status"] = "completed"
save_data(data)
```

In the full program, select a book from the list of books currently in progress before updating it.

## Step 5: Set a monthly goal

BookQuest starts with a goal of four books per month. You can change the goal and save it:

```python
goal = int(input("Enter your monthly book target: "))

if goal >= 1:
    data["monthly_goal"] = goal
    save_data(data)
```

The complete program should also handle invalid input, such as text instead of a number.

## Step 6: Count books completed each month

We can use the first seven characters of a finish date, such as `2026-10`, as a month key.

```python
totals = {}

for book in data["books"]:
    finish_date = book.get("finish_date")

    if finish_date:
        month = finish_date[:7]
        totals[month] = totals.get(month, 0) + 1
```

This creates a dictionary containing the number of completed books per month. Books that are still in progress are excluded.

## Step 7: Display reading statistics

Easy Stats provides helpers for summarizing the monthly totals:

```python
counts = list(totals.values())

if counts:
    print("Median monthly total:", median(counts))
    print("Monthly total range:", data_range(counts))

if len(counts) >= 2:
    print("Standard deviation:", standard_deviation(counts))
```

- `median()` returns the middle value of the monthly totals.
- `data_range()` returns the difference between the highest and lowest totals.
- `standard_deviation()` measures how spread out the totals are.

These statistics describe completed books per month, not books currently being read.

## Step 8: Display a friendly date

Use Easy Date Formatter to show today's date in a readable format:

```python
print("Reading summary for", get_pretty_date())
```

The start and finish dates remain in ISO format so they can be grouped by month.

## Step 9: Visualize monthly reading activity

Once monthly totals have been calculated, use the appropriate chart helper to display the results. For a month-labelled chart, use a dedicated chart function with month labels and corresponding counts, after confirming its supported parameters in your installed version.

The chart should compare books completed across months, rather than imply that an entire book is finished each day.

## Test your project

1. Add two books.
2. View your reading shelf.
3. Mark one book as completed.
4. Change your monthly goal.
5. Open the reading summary.
6. Exit and run the application again.
7. Confirm that the books and goal are still saved.

## What happened?

You combined JSON storage, date formatting, statistics, and visualization to create a small reading tracker. Each helper handles a common task, leaving the application code to focus on managing books and displaying progress.

## Why use these helpers?

Without `py_simple`, you would need to write more of the file handling, date formatting, statistical calculations, and plotting setup yourself. These helpers make the project easier to read and provide a practical example of multiple modules working together.
