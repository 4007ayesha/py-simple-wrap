# Building a Screen Time Detective with Easy CSV and Easy Data Visualization

Combine **Easy CSV** and **Easy Data Visualization** to turn a week of phone usage data into charts in just a few lines of Python.

## What we are building

Ever wondered how much time you *actually* spend on your phone? We'll log a week of screen time in a spreadsheet, then let Python read it and draw charts showing which day was the worst and which app wins most often.

First, save this as `screen_time.csv` in the same folder as your script:

```text
day,hours,top_app
Mon,3.5,TikTok
Tue,2.0,YouTube
Wed,4.5,TikTok
Thu,1.5,Spotify
Fri,5.0,YouTube
Sat,6.5,TikTok
Sun,4.0,Instagram
```

Then create `detective.py`:

```python
from py_simple import read_csv_to_list, plot_data

# 1. Read the spreadsheet into a list of rows
rows = read_csv_to_list("screen_time.csv")

# 2. Pull out each column we care about
days = [row["day"] for row in rows]
hours = [float(row["hours"]) for row in rows]
apps = [row["top_app"] for row in rows]

# 3. Print the week's total
print(f"Total screen time this week: {sum(hours)} hours")

# 4. Chart hours per day, then which app was the top app most often
plot_data(days, hours)
plot_data(apps)
```

Run it and you'll see your weekly total, a bar chart of hours per day, and then a bar chart and pie chart of your top apps.

## What happened?

1. `read_csv_to_list("screen_time.csv")` opens the file and returns every row as a dictionary, so you can grab values by column name like `row["hours"]`.
2. The list comprehensions pull each column into its own list. CSV values come in as text, so `float()` turns the hours into numbers.
3. `sum(hours)` adds up the whole week.
4. `plot_data(days, hours)` notices that `days` are labels and `hours` are numbers, so it automatically picks a bar chart.
5. `plot_data(apps)` sees a single list of labels, so it counts them and shows a bar chart and a pie chart side by side.

## Why use these helpers?

Doing this with raw Python and matplotlib usually means:
- Importing the `csv` module, opening the file with `with open(...)`, and wrapping it in a `csv.DictReader`.
- Counting how often each app appears yourself before you can chart it.
- Creating figures and axes, choosing the right chart type, and calling `plt.show()`.

By combining `easy_csv` and `easy_data_visualization`, reading the data and picking the right chart each take one line, so you can focus on the fun part: finding out Saturday was a 6.5-hour day.
