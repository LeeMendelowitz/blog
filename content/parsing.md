Title: Parsing in Python
Date: 2013-10-3 22:07
Slug: parsing-in-python
Category: Python
Tags: python
Author: Lee Mendelowitz
Summary: How to parse in python

In Python, everything is an object. Even the built-in types themselves
(i.e. int, str, dict, list, etc.) are object's of type type. 
You can use the built-in type function to get an object's type.

    :::python
    type(int) # Returns type. So int is an object of type type.
    isinstance(int, type) # Returns True
    isinstance(int, object) # Returns True
    type(type) # Returns type. So type is an object of type type. Truth.
    type(object) # Returns type. So object is an object of type type. Mind blown.

Since everything in Python is an object, you can treat them as such. This means you can store the types themselves in a list.

    :::python
    my_types = [int, float, str, dict]

It turns out this is really useful when writing scripts to parse a text file.
Let's say I'm writing a script to parse the CSV file below. (In reality,
I should just use the [pandas](http://pandas.pydata.org/) library.)

    :::text
    Bob, Jones, 26, 184.2
    Thomas, Apple, 19, 155.9
    Jake, Wilson, 31, 172.2

The parser script can store the types of each field in a list,
and utilize it to convert each field value to its appropriate type
with a simple generator expression:

    :::python
    field_names = ['first', 'last', 'age', 'weight']
    field_types = [str, str, int, float]

    def parse_line(l):
        """
        Parse a single line and return a dictionary.
        """
        field_values = l.split(',')
        return dict((fn, ft(fv)) for fn,ft,fv in zip(field_names, field_types, field_values))

    def parse(filename):
        """
        Parse all of the lines in the file.
        """
        return [parse_line(l) for l in open(filename)]

To summarize, storing types in a list is really useful for writing concise scripts to parse text.
