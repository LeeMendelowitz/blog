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


Here is the [source](https://gist.github.com/LeeMendelowitz/36941676def5c521a960) for the decorator, which also takes care to close any files it opens
in the event that the wrapped function throws an exception:

```python
class wrap_file_function(object):
  """
  Wrap a function which takes a file or a str as it's first argument.
  If a str is provided, replace the first argument of the wrapped function
  with a file handle, and close the file afterwards

  Example:

  @wrap_file_function('w')
  def write_hi(f):
    f.write('hi!\n')

  # This will write to already open file handle.
  f = open('f1.txt', 'w')
  write_hi(f)
  f.close()

  # This will open file f2.txt with mode 'w', write to it, and close the file.
  write_hi('f2.txt')
  """

  def __init__(self, *args):
    self.modes = args if args else ('r',)

  def __call__(self, func):

    def wrapped(*args, **kwargs):

      close = [] # Files that should be closed
      files = [] # File handles that should be passed to func
      num_files = len(self.modes)

      try:

        for i, mode in enumerate(self.modes):

          fp = args[i]

          if isinstance(fp, str):
            fp = open(fp, mode)
            close.append(fp)

          files.append(fp)

        # Replace the files in args when calling func
        args = files + list(args[num_files:])

        # Make function call and return value
        return func(*args, **kwargs)

      finally:

        for fp in close:
            fp.close()

    return wrapped



if __name__ == "__main__":
 
  # Demonstration of wrapping a function which writes to a file.
  print '-'*50
  @wrap_file_function('w')
  def write_hi(f):
    f.write('hi!\n')
 
  f = open('temp.txt', 'w')
  write_hi(f)
  write_hi(f)
  write_hi(f)
  f.close()
 
  write_hi('temp2.txt')
  
 
  # Demonstration of wrapping a function which reads from a file.
  print '-'*50
  @wrap_file_function()
  def read_file(f):
      print f.read()
 
  f = open('temp.txt')
  print 'Reading file temp.txt from handle f:'
  read_file(f)
  print 'Reading file temp2.txt'
  read_file('temp2.txt')

  # Demonstration of wrapping a function takes multiple files
  print '-'*50
  @wrap_file_function('r', 'r')
  def read_files(f1, f2):
      print 'reading f1: '
      print f1.read()
      print 'reading f2: '
      print f2.read()

  @wrap_file_function('r', 'w')
  def read_write(f1, f2):
    f2.write(f1.read())
 
  @wrap_file_function('w', 'r')
  def write_to_from(f2, f1):
    f2.write(f1.read())

  read_files(open('temp.txt'), open('temp2.txt'))
  read_files('temp.txt', 'temp2.txt')
  read_write('temp.txt', 'temp.copy.txt')

  import sys
  print 'writing temp.txt to stdout:'
  read_write('temp.txt', sys.stdout)

  print 'Contents of temp.copy.txt:'
  read_file('temp.copy.txt')

  @wrap_file_function('w')
  def throw_exception(f):
    raise RuntimeError('BLAH!')

  print '-'*50
  print 'Reading a file that does not exist:'
  write_to_from('dest.txt', 'file_doesnt_exist.txt')

  #print '-'*50
  #throw_exception('exception.txt')
```

<!-- the gist styles look bad! Instead, we'll just paste the source --!>
<!-- <script src="https://gist.github.com/LeeMendelowitz/36941676def5c521a960.js"></script> -->
<!-- [gist:id=36941676def5c521a960] -->
