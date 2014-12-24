Title: std::sort and std::bad_alloc
Date: 2014-12-23 22:02
Slug: sort-bad-alloc
Category: C++
Tags: C++
Author: Lee Mendelowitz
Summary: Painful reminder of why programming in C++ can be hard.

Sometimes programming in C++ is wonderful when everything works and programs run blazingly fast, and then there are those painful moments when you encounter hard to diagnose runtime errors.

In this case, I was calling `std::sort` to sort a `std::vector` of `Alignment` objects.
I was using my own custom compare class to determine when one `Alignment` object should appear before the other.

The sort failed by throwing a `std::bad_alloc` exception, which is [thrown when failing to allocate memory](http://www.cplusplus.com/reference/new/bad_alloc/).

I was baffled for quite a while and had to step into the `gdb` debugger to get a very long backtrace with all of the gory details.

After quite some time, it boiled down to the fact that I had a bug in the `Alignment`assignment operator: `Alignment& operator=(const Alignment& a)`. This buggy assignment operator did not properly assign all of the attributes of the `Alignment` object - in particular it failed to properly assign the attribute being sorted on (oops!) - and this had the effect of violating the strict weak ordering which `std::sort` requires of the compare operator. This, in turn, somehow resulted in the `std::bad_alloc` exception. 

It turns out I did not even need to provide a custom assignment operator - the default provided by the compiler would do.

For future reference, here's a [Stack Overflow](http://stackoverflow.com/questions/9170080/stdsort-getting-a-stdbad-alloc) post where someone else encountered the same thing.

Like I said, C++ can be painful.


