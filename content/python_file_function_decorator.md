Title: Decorating Python File Functions
Date: 2014-04-30 16:45
Slug: decorating-python-file-functions
Category: Python
Tags: python
Author: Lee Mendelowitz
Summary: How to wrap a Python function which writes to a file.

Today I came up with a cool Python snippet that I'd like to share.
In my work I frequently write functions which write to or read from files, taking a `file`-like
instance as the first argument `f`:

    :::python
    def write_to_file(f):
        f.write('hi!\n')


To make things more flexible, we can modify the function to accept a `file`-like instance or
a `str` specifying the path to the file to open:

    :::python
    def write_to_file_ver2(f):
        close = False
        if isinstance(f, str):
            f = open(f, 'w') 
            close = True

        f.write('hi!\n')

        if close:
            f.close()

Now we can pass this function a `file` or a `str` with a file path:

    :::python
    f = open('hi.txt', 'w')
    write_to_file_ver2(f)
    f.close()

    # Or

    write_to_file_ver2('hi.txt')

This pattern is common enough that it's worth creating a decorator for it. We can wrap functions so they 
accept either a `file`-like handle as the first argument, or a `str` to a file.

The decorated function `write_hi_ver3` below is identical to `write_hi_ver2` above, but with less code.

    :::python
    @wrap_file_function('w')
    def write_hi_ver_3(f):
        f.write('hi!\n')

The decorator can also wrap a function which takes multiple file handles by specifiying
multiple file access modes: 

    :::python
    @wrap_file_function('r', 'w')
    def copy_file(f1, f2):
        f2.write(f1.read())

    copy_file('hi.txt', 'hi.copy.txt')


Here is the source for the decorator, which also takes care to close any files it opens
in the event that the wrapped function throws an exception.

[gist:id=36941676def5c521a960]
