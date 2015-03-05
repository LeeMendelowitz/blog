Title: Scraping data from dynamic webpages with PhantomJS
Date: 2015-02-25 23:00
Slug: scraping-data-from-dynamic-webpages
Author: Lee Mendelowitz
Tags: R
Summary: How to scrape data from dynamic webpages using PhantomJS
Status: draft


The `readHTMLTable` function in R from the WHATEVER package is really useful for
quickly grabbing data from a webpage and formatting it into a `data.frame`. However, this only works if the table is embedded in the html page source. More and more webpages today have content that is injected dynamically into the page using javascript. This makes it much more difficult to scrape data from a webpage.

Fortunately, there are still ways to scrape data from dynamic pages. PhantomJS is a really cool tool which works as a "headless" browser (i.e. without a display). PhantomJS can load webpage, execute the javascript on that page, and 


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

