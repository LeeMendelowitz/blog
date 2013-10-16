Title: Mathematical expressions in plots
Date: 2013/10/15
Category: R
Tags: R, Computing For Data Analysis
Author: Lee Mendelowitz

[Download as R Markdown]({filename}rmarkdown/plotmath.rmd).

Mathematical expressions can be included in the plot title or axis labels. For more information, see `?plotmath` or run the demo with `demo(plotmath)`.

Here are some quick examples.





### Example 1 ###


```r
plot(0, 0, main = expression(theta == 0), ylab = expression(hat(gamma) == 0), 
    xlab = expression(sum(x[i] * y[i], i == 1, n)))
```

![plot of chunk example1]({filename}figure/plotmath_example1.png) 


### Example 2 ###

Strings can be pasted together with mathematic expressions:


```r
x <- rnorm(100)
hist(x, xlab = expression("The mean (" * bar(x) * ") is " * sum(x[i]/n, i == 
    1, n)))
```

![plot of chunk example2]({filename}figure/plotmath_example2.png) 


### Example 3 ###
The `subsitute` function can be used to substitute values into a
mathematical expression.

```r
x <- rnorm(100)
y <- x + rnorm(100, sd = 0.5)
plot(x, y, xlab = substitute(bar(x) == k, list(k = mean(x))), ylab = substitute(bar(y) == 
    k, list(k = mean(y))))
```

![plot of chunk example3]({filename}figure/plotmath_example3.png) 

