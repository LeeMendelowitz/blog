Title: Python OS X Mavericks Issues
Date: 2014-03-29 2:00
Slug: python-mavericks-issues
Author: Lee Mendelowitz
Tags: python
Summary: Some issues I encountered with my Python installation after upgrading to OS X Mavericks.

Yesterday I decided to upgrade OS X on my Late-2011 Mac Book Pro from 10.7 Lion to 10.9 Mavericks. I felt no rush to upgrade - "If it ain't broke, don't fix it!" - but after reading about the new features, particularly the improved support for multiple displays - I decided to give it a shot.

Everything went smoothly - except that my Python installation completely broke. This was a big break - I work in Python almost everyday. By broke, I mean that Apple wiped out all of the python libraries I've installed - pip, virtualenv, numpy, matplotlib, ipython, pandas, flask, greenlet - all gone.

In retrospect, it was my mistake. I was installing packages in `/Library/Python/2.7/site-packages`, which Apple wiped clean when I upgraded to Mavericks.

I recovered by installing Python using Homebrew. It's a much better option because:

- the installation will come with `pip` installed
- the Python packages you install will be put in a safe place and you won't need to use `sudo` to install them.
- You'll avoid some compilation errors when installing some packages.
     - I encountered [this](http://stackoverflow.com/questions/22313407/clang-error-unknown-argument-mno-fused-madd-python-package-installation-fa) issue when trying to install `greenlet` package using an `easy_install`'ed version of' `pip`, but **not** with the Homebrew installed `pip`.

Here are the steps I followed to fix my Python installation:

1. You need to reinstall XCode and the Command Line Tools to get a compiler. This can be done from the App Store. Lots of resources on how to do this - see [this](http://railsapps.github.io/xcode-command-line-tools.html) or [this](http://railsapps.github.io/xcode-command-line-tools.html).

2. Install Python with [Homebrew](http://brew.sh) instead of using the Python interpreter which ships with Mavericks. Homebrew will install the latest Python v2.7.6, while Mavericks ships with v2.7.5:

        :::bash
        brew update
        brew install python 

3. Upgrade setuptools and pip, as suggested:

        :::bash
        pip install --upgrade setuptools
        pip install --upgrade pip
        

4. Install your favorite package

        :::bash
        pip install numpy, ipython, matplotlib, pandas, flask, yolk
    

These will be installed to `/usr/local/lib/python2.7/site-packages`, which is a safe zone. Future OS X upgrades won't wipe out your installed packages.

I'm still getting build errors on scipy that I have not yet resolved, but I'll save that for another rainy day.

In conclusion, use Homebrew to stay *mostly* sane.