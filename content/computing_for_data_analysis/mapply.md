Title: mapply
Date: 2013/10/13
Category: R
Tags: R, Computing For Data Analysis
Author: Lee Mendelowitz

<!--- mapply -->

[Download as R Markdown]({filename}rmarkdown/mapply.rmd).


`mapply` gives us a way to call a non-vectorized function in a vectorized way.

From the R Documentation:

```
mapply is a multivariate version of sapply. mapply applies FUN to
the first elements of each ... argument, the second elements,
the third elements, and so on. Arguments are recycled if necessary.

mapply(FUN, ..., MoreArgs = NULL, SIMPLIFY = TRUE,
       USE.NAMES = TRUE)
```

### Example ###


```r
list(rep(1, 4), rep(2, 3), rep(3, 2), rep(4, 1))
```

```
## [[1]]
## [1] 1 1 1 1
## 
## [[2]]
## [1] 2 2 2
## 
## [[3]]
## [1] 3 3
## 
## [[4]]
## [1] 4
```


We see that we are repeatedly calling the same function (`rep`) where the first argument varies from 1 to 4, and the second argument varies from 4 to 1.
Instead, we can use `mapply`:


```r
mapply(rep, 1:4, 4:1)
```

```
## [[1]]
## [1] 1 1 1 1
## 
## [[2]]
## [1] 2 2 2
## 
## [[3]]
## [1] 3 3
## 
## [[4]]
## [1] 4
```


### Example ###


```r
noise <- function(n, mean, std) {
    rnorm(n, mean, std)
}
noise(5, 1, 2)
```

```
## [1] 0.84136 0.04806 1.89196 2.76464 4.95360
```


The noise function is not vectorized. `mapply` gives us a way to make a vectorized call to  `noise`:


```r
mapply(noise, 1:5, 1:5, 2)
```

```
## [[1]]
## [1] 1.625
## 
## [[2]]
## [1]  2.928 -1.840
## 
## [[3]]
## [1] 2.459 4.195 1.939
## 
## [[4]]
## [1] 5.195 3.731 5.249 2.959
## 
## [[5]]
## [1] 8.291 1.949 5.751 4.250 4.868
```

