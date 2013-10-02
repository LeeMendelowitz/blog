Title: Wrapping Python Dictionaries
Date: 2013-10-2 17:45
Slug: wrapping-python-dictionaries
Category: Python
Tags: python, ipython
Author: Lee Mendelowitz
Summary: How to wrap a python dictionary for IPython autocompletion.

Very frequently when I'm programming in python, I write functions that return a
dictionary with string keys.

When developing or debugging such programs in IPython, it's pretty tedious to
inspect these dictionaries. First, you need to get a list of keys. Then, to see a particular
value in the dictionary ```d```, you need to type out ```d['key']```. It gets tedious
after a while.

IPython has really useful object introspection and tab-completion features, but they aren't
useful in this situation. A simple hack is to implement a class which sets the instance attributes
using the key/value pairs stored in a dictionary.

    :::python
    class DictWrap(object):
        """
        Class to wrap a python dictionary.
        This helps with tab completion for object introspection in IPython

            myD = {'one' : 1, 'two' : 2}
            d = DictWrap(myD)

        Now in IPython you can inspect and autocomplete with d.o<TAB>
        """

        def __init__(self, d):
            """
            Construct a DictWrap instance from a python dictionary d
            """
            for k,v in d.iteritems():
                setattr(self, k, v)

Now in the IPython shell, you can easily inspect your dictionaries using tab-completion!

    :::python
    myD = {'one' : 1, 'two' : 2, 'three' : 3}
    d = DictWrap(myD)
    d.<TAB> # prints d.one d.two d.three
    d.t<TAB> # prints d.two d.three
