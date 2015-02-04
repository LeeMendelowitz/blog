Title: Fix the pesky "^M" carriage return control character using tr
Date: 2015-02-04 3:20
Slug: remove-carriage-return-control-character
Author: Lee Mendelowitz
Tags: python
Summary: How to fix the "^M" carriage return control character using tr

When working with Microsoft Excel 2011 on Mac OS X, it will export spreadsheets to comma separated .csv files or
tab delimited .txt plain text files using the old Mac OS 9 line endings of a carriage return (`\r`).
When viewed with `less` or `vi`, these characters appear as `^M`, and the text file appears as one massively long line.

These end of line characters can be handled when importing data using R or Python's pandas library, but it's still a 
nuisance for other common Unix utilities like GNU's `head`, `tail`, `less`, `wc -l`, etc.

There are a few ways to convert these line endings using GNU utilities. You can use `tr` or `dos2unix`. 

# Using tr

### Mac (`\r`) to Unix (`\n`)

To replace those `^M`'s with Unix line endings, use the `tr` utility:

```bash
tr '\r' '\n' < DC_Metrorail_Ridership.mac.csv > DC_Metrorail_Ridership.unix.csv
```

This will replace all carriage returns with line feeds.

### Windows (`\r\n`) to Unix (`\n`)

Windows line endings use carriage return followed by line feed, so to convert Microsoft text files line endings to Unix use the following:

```bash
tr -d '\r' < DC_Metrorail_Ridership.windows.csv > DC_Metrorail_Ridership.unix.csv
```

# Using dos2unix or mac2unix

Another option is to use the `dos2unix` utility. To install on Mac OS X using Homebrew:

```bash
brew update
brew install dos2unix
```

### Mac (`\r`) to Unix (`\n`)

```bash
mac2unix -n DC_Metrorail_Ridership.mac.csv DC_Metrorail_Ridership.unix.csv
```

### Windows (`\r\n`) to Unix (`\n`)
```bash
dos2unix -n DC_Metrorail_Ridership.windows.csv DC_Metrorail_Ridership.unix.csv
```

I made a [GitHub gist](https://gist.github.com/LeeMendelowitz/7509ae7cfeaf1072822a) where you can test all of this out. Clone the gist with:

```bash
git clone https://gist.github.com/7509ae7cfeaf1072822a.git
```

