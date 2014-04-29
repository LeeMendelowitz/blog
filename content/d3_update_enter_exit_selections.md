Title: D3 Update Enter Exit Selections
Date: 2014-04-28 12:00
Slug: d3-update-enter-exit-selections
Author: Lee Mendelowitz
Tags: d3, javascript
Summary: A demo on D3's update, enter, and exit selections.

Lately I've been playing around with the D3 javascript library for data visualizations in a browser. D3 stands for "Data Driven Documents" and provides utilities for manipulating elements on a webpage based on data. The D3 [gallery](https://github.com/mbostock/d3/wiki/Gallery) is very impressive.

I've had trouble wrapping my head around the update, enter, and exit selections, which provide a mechanism for updating, inserting, and removing elements from a page based on changes in data.

There are already some great [tutorials](https://github.com/mbostock/d3/wiki/Tutorials) by Mike Bostock and others on [joins](http://bost.ocks.org/mike/join/), [updates](http://bl.ocks.org/mbostock/3808234) and [selections](http://bost.ocks.org/mike/selection/).

I challenged myself to create a demo which illustrates populating a table with changing data using the full update pattern. The table is a little more challenging because the data is nested; data is first bound to each row as an array of values, then data is bound to each cell of the row as a single value. We have to handle cases where cells are added to or deleted from existing rows, and where entire rows are added or deleted.

You can see the demo below and check out the source [here](http://bl.ocks.org/LeeMendelowitz/11383724).

<iframe src="code/d3_updating_table.html" marginwidth="0" marginheight="0" width="600" height="1000"></iframe>