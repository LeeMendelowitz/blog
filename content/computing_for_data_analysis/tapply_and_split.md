Title: tapply and split
Date: 2013/10/13
Category: R
Tags: R, Computing For Data Analysis
Author: Lee Mendelowitz

<!--- tapply and split -->

[Download as R Markdown]({filename}rmarkdown/tapply_and_split.rmd).




## tapply ##

Apply a function over subsets of a vector.

### Example: Take group means with tapply. ###




```r
x <- c(rnorm(10), runif(10), rnorm(10, 1))
x
```

```
##  [1] -2.04333  0.72651  1.55476 -0.12411  1.08133 -0.30514  1.38638
##  [8]  0.35047  0.88147  1.80250  0.56072  0.54421  0.19270  0.67049
## [15]  0.83034  0.02640  0.98629  0.11223  0.10747  0.85049  1.37510
## [22]  0.56575  0.34138  1.01877  1.33956 -0.07667  2.12114  0.70827
## [29]  0.53336  2.15315
```

```r
f <- gl(3, 10)  # Generator factors
f
```

```
##  [1] 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 3 3 3 3 3 3 3 3 3 3
## Levels: 1 2 3
```

By default, if the applied function returns a scalar, then tapply
returns a vector. In this case we are applying the mean function,
so the output of tapply is a numeric vector.

```r
tapply(x, f, mean)  # Take the mean of each group. Returns a vector.
```

```
##      1      2      3 
## 0.5311 0.4881 1.0080
```


Without simplification, tapply always returns a list.


```r
tapply(x, f, mean, simplify = FALSE)
```

```
## $`1`
## [1] 0.5311
## 
## $`2`
## [1] 0.4881
## 
## $`3`
## [1] 1.008
```


### Example: Find the group range ###

Range returns the minimum and maximum value for each group.
Note that since the range function returns a vector, tapply returns
a list.


```r
tapply(x, f, range)
```

```
## $`1`
## [1] -2.043  1.803
## 
## $`2`
## [1] 0.0264 0.9863
## 
## $`3`
## [1] -0.07667  2.15315
```


## split ##

The split function splits a vector int groups using a factor.
Using split and then applying a function with lapply produces the same 
resule as tapply:


```r
split(x, f)
```

```
## $`1`
##  [1] -2.0433  0.7265  1.5548 -0.1241  1.0813 -0.3051  1.3864  0.3505
##  [9]  0.8815  1.8025
## 
## $`2`
##  [1] 0.5607 0.5442 0.1927 0.6705 0.8303 0.0264 0.9863 0.1122 0.1075 0.8505
## 
## $`3`
##  [1]  1.37510  0.56575  0.34138  1.01877  1.33956 -0.07667  2.12114
##  [8]  0.70827  0.53336  2.15315
```

```r
lapply(split(x, f), mean)  # Instead of tapply
```

```
## $`1`
## [1] 0.5311
## 
## $`2`
## [1] 0.4881
## 
## $`3`
## [1] 1.008
```


### Example: Air Quality by month ###


```r
library(datasets)
head(airquality)
```

```
##   Ozone Solar.R Wind Temp Month Day
## 1    41     190  7.4   67     5   1
## 2    36     118  8.0   72     5   2
## 3    12     149 12.6   74     5   3
## 4    18     313 11.5   62     5   4
## 5    NA      NA 14.3   56     5   5
## 6    28      NA 14.9   66     5   6
```

```r
s <- split(airquality, airquality$Month)
```


`s` is a list of dataframes split by month:


```r
class(s)
```

```
## [1] "list"
```

```r
class(s[[1]])
```

```
## [1] "data.frame"
```

```r
lapply(s, function(x) head(x, n = 2))
```

```
## $`5`
##   Ozone Solar.R Wind Temp Month Day
## 1    41     190  7.4   67     5   1
## 2    36     118  8.0   72     5   2
## 
## $`6`
##    Ozone Solar.R Wind Temp Month Day
## 32    NA     286  8.6   78     6   1
## 33    NA     287  9.7   74     6   2
## 
## $`7`
##    Ozone Solar.R Wind Temp Month Day
## 62   135     269  4.1   84     7   1
## 63    49     248  9.2   85     7   2
## 
## $`8`
##    Ozone Solar.R Wind Temp Month Day
## 93    39      83  6.9   81     8   1
## 94     9      24 13.8   81     8   2
## 
## $`9`
##     Ozone Solar.R Wind Temp Month Day
## 124    96     167  6.9   91     9   1
## 125    78     197  5.1   92     9   2
```



After splitting by month, we can use `lapply` to take the column means:


```r
takeMeans <- function(x) colMeans(x[, c("Ozone", "Solar.R", "Wind")], na.rm = TRUE)
lapply(s, takeMeans)
```

```
## $`5`
##   Ozone Solar.R    Wind 
##   23.62  181.30   11.62 
## 
## $`6`
##   Ozone Solar.R    Wind 
##   29.44  190.17   10.27 
## 
## $`7`
##   Ozone Solar.R    Wind 
##  59.115 216.484   8.942 
## 
## $`8`
##   Ozone Solar.R    Wind 
##  59.962 171.857   8.794 
## 
## $`9`
##   Ozone Solar.R    Wind 
##   31.45  167.43   10.18
```


Using `sapply` instead of `lapply` simplifies the output into a matrix,
so we can easily see the mean values by month.


```r
sapply(s, takeMeans)
```

```
##              5      6       7       8      9
## Ozone    23.62  29.44  59.115  59.962  31.45
## Solar.R 181.30 190.17 216.484 171.857 167.43
## Wind     11.62  10.27   8.942   8.794  10.18
```


### Splitting on more than one level ###


```r
x <- rnorm(10)
f1 <- gl(2, 5)  # Create a factor with two levels
f2 <- gl(5, 2)  # Create a factor with five levels
str(f1)
```

```
##  Factor w/ 2 levels "1","2": 1 1 1 1 1 2 2 2 2 2
```

```r
str(f2)
```

```
##  Factor w/ 5 levels "1","2","3","4",..: 1 1 2 2 3 3 4 4 5 5
```

```r
interaction(f1, f2)  # Compute a factor with 10 levels, which is the interaction of the two factors
```

```
##  [1] 1.1 1.1 1.2 1.2 1.3 2.3 2.4 2.4 2.5 2.5
## Levels: 1.1 2.1 1.2 2.2 1.3 2.3 1.4 2.4 1.5 2.5
```


Note that some levels of the interaction are empty for our data vector `x`. For example, none of the samples in `x` have level 2.1.

We can use multiple factor levels with `split` by passing the interaction
factor. Instead of calling `interaction` explicitly, if we pass the factors in a list, the `interaction` function is automatically called:


```r
str(split(x, list(f1, f2)))  # Automatically calls interaction(f1,f2)
```

```
## List of 10
##  $ 1.1: num [1:2] 0.993 0.939
##  $ 2.1: num(0) 
##  $ 1.2: num [1:2] 1.092 -0.382
##  $ 2.2: num(0) 
##  $ 1.3: num -0.985
##  $ 2.3: num 1.53
##  $ 1.4: num(0) 
##  $ 2.4: num [1:2] -0.066 -1.64
##  $ 1.5: num(0) 
##  $ 2.5: num [1:2] 0.452 -1.324
```


Note that some levels are empty, but they still appear in list output by
`split`.  Empty levels can be dropped by passing  `drop = TRUE`.


```r
str(split(x, list(f1, f2), drop = TRUE))
```

```
## List of 6
##  $ 1.1: num [1:2] 0.993 0.939
##  $ 1.2: num [1:2] 1.092 -0.382
##  $ 1.3: num -0.985
##  $ 2.3: num 1.53
##  $ 2.4: num [1:2] -0.066 -1.64
##  $ 2.5: num [1:2] 0.452 -1.324
```

