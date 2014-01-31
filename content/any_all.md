Title: Any and All
Date: 2014-1-31 12:42
Slug: any-all-in-python
Category: Python
Tags: python
Author: Lee Mendelowitz
Summary: Demonstration of any/all in Python.

Here's an [ipython notebook](http://nbviewer.ipython.org/gist/LeeMendelowitz/8738004) with the code for this post, and the ipython notebook [source](https://gist.github.com/LeeMendelowitz/8738004).

`any` and `all` are useful Python functions. Given an iterable (like a list, a generator, an str, etc.), these functions check if any or all of the values are True (or "truthy"). Here is a simple example where we are checking the values of the letters in the word "python":

    :::python
    any(l == 't' for l in 'python') # Returns True. Same as: 't' in 'python'
    all(l == 't' for l in 'python') # Returns False. Not all of the letters are 't'.

This seems like a simple function call, but things are slightly more complicated than they look.

First, a generator is constructed from the expression `l == 't' for l in 'python'`. What is a generator? A generator is an object which is both an iterator (has the `next` method) and is also iterable (has the `__iter__` method which returns an iterator). Strings themselves are iterable, which is how the `for l in 'python'` part works.

You can define a generator through a generator expression:

    :::python
    g = (l == 't' for l in 'python')

Note that a generator expression is similar to a list comprehension, except uses parentheses instead of brackets. A key difference is that while a list comprehension immediately computes all of the values and stores them in a list in memory, a generator expression generates its values lazily on demand.

To show that `g` is an iterator, we can get the first few values by hand:

    :::python
    print g.next() # False. 'p' is not equal to 't'
    print g.next() # False. 'y' is not equal to 't'
    print g.next() # True. 't' is equal to 't'

Again, these True/False responses are lazily computed by the generator only upon demand. You can also use `g` in a loop, since it's iterable. Under the hood, the `for` loop calls the `__iter__` function of g:

    :::python
    g = (l == 't' for l in 'python')
    for value in g:
        print value

Functions that accept iterable objects, like `any` and `all`, will accept a generator expression:

    :::python
    g = (l == 't' for l in 'python')
    any(g)
    any( (l == 't' for l in 'python') ) # same thing

Finally, python lets us avoid the "double parentheses" when we pass a generator expression to a function call:

    :::python
    any(l == 'l' for l in 'hello') # same thing as any((l == 't' for l in 'python'))

So that's how the function call itself works. How do `any` and `all` work with the iterable it is given? 

Let's demonstrate this with a simple example:

    :::python
    def t():
        print 'In True!'
        return True

    def f():
        print 'In False!'
        return False

    # Store functions to be called in a list
    funcs = [t, f, f, f, t]

    def test_any():
        # Pass a generator expression with function calls to any
        print any(func() for func in funcs)

    def test_all():
        # Pass a generator expression with function calls to all
        print all(func() for func in funcs)

    test_any() # Calls t() once and stops.
    test_all() # Calls t(), then f(), then stops

In this example, `any` stopped after the first True value it sees, and 
`all` stopped after the first False value. This makes sense - both `any` and `all` can stop
iterating over their argument once they've figured out their return value. 

The more you know!