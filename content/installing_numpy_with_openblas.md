Title: Installing Numpy with OpenBlas
Date: 2014-10-23 9:20
Slug: installing-numpy-with-openblas
Category: misc
Tags: python, numpy
Author: Lee Mendelowitz
Summary: How to install numpy with OpenBlas.

I just went through the frustrating but in the end rewarding experience of trying to install numpy in my school computing RHEL5 environment where I don't have sudo privileges or much control over the environment. In the end, I learned quite a bit!

My first attempt to install was through the normal path, where I activate a virtual environment created with `virtualenv` and then use pip to install numpy:

```bash
cd ~
virtualenv venv
source venv/bin/activate
pip install numpy
```

But trying to build numpy in my environment led to this error:

```
ImportError: home/venv/lib/python2.7/site-packages/numpy/linalg/lapack_lite.so: undefined symbol: zgelsd_
```

So that's the clue - something is wrong with the lapack library numpy is trying to use from my environment. It's probably linked against something broken or something incompatible... or something missing.

Here's what `ldd` on the **broken** lapack_lite.so gives:

```bash
ldd home/venv/lib/python2.7/site-packages/numpy/linalg/lapack_lite.so
        linux-vdso.so.1 =>  (0x00007fff08126000)
        libpython2.7.so.1.0 => not found
        libpthread.so.0 => /lib64/libpthread.so.0 (0x00002b39c2bc9000)
        libc.so.6 => /lib64/libc.so.6 (0x00002b39c2de5000)
        /lib64/ld-linux-x86-64.so.2 (0x0000003185e00000)
```

So, after some searching around, it seems like the best option was to compile the [OpenBlas](https://github.com/xianyi/OpenBLAS) library and use that during the numpy build. I was able to salvage bits from [this](https://gist.github.com/sniderbr/5891950), and [this](http://gromgull.net/blog/2013/07/multithreaded-scipynumpy-with-openblas-on-debian/) to get it to work.


# Build OpenBlas

Untar the OpenBlas distribution [available here](http://www.openblas.net/) and build using the makefile:

```bash
make BINARY=64 FC=gfortran USE_THREAD=1
make PREFIX=/path/to/openblas install
```

where `/path/to/openblas` is the path where you'd like to install openblas. Again, since I did have `sudo` privilegs, I chose a non-standard location.

# Build Numpy

We need to build numpy and link it with the OpenBlas library. I couldn't achieve this with the default `pip` install, so things had to be done manually as suggested in [this post](http://gromgull.net/blog/2013/07/multithreaded-scipynumpy-with-openblas-on-debian/):

```bash
source venv/bin/activate
pip uninstall numpy # Uninstall the broken installation
mkdir venv/download
pip install -d venv/download numpy
mkdir venv/build
cd venv/build
tar xzf ../download/numpy-1.9.0.tar.gz
cd numpy-1.9.0
```

In the `numpy-1.9.0` directory, create the `site.cfg` file to customize the libraries that numpy uses on install. We need to point things to OpenBlas. Check out the `site.cfg.example` file for what options you can set. This worked for me:  

```bash
[DEFAULT]
library_dirs = /path/to/openblas/lib
include_dirs = /path/to/openblas/include

[atlas]
atlas_libs = openblas
libraries = openblas

[openblas]
libraries = openblas
library_dirs =  /path/to/openblas/lib
include_dirs =  /path/to/openblas/include
```

Next, build numpy **being sure to specify the same fortran compiler that was used to build the OpenBlas library** (important point mentioned in the [scipy install docs](http://docs.scipy.org/doc/numpy/user/install.html)). For good measure, I cleaned out all of the standard compile and linking flags from my environment to make sure I wasn't contaminating the build:

```bash
unset CPPFLAGS
unset LDFLAGS
python setup.py build --fcompiler=gnu95
```

When the build completes, install:
```bash
python setup.py install
```

Since the virtual environment is active, this will install to the virtual environment.

Finally, here's what `ldd` on the working `lapack_lite.so` library gives:

```
ldd home/venv/lib/python2.7/site-packages/numpy/linalg/lapack_lite.so
(venv)bash-3.2$ ldd lapack_lite.so
        linux-vdso.so.1 =>  (0x00007ffff40b9000)
        libopenblas.so.0 => ../lib/libopenblas.so.0 (0x00002b098e0a1000)
        libpython2.7.so.1.0 => not found
        libgfortran.so.3 => .../libgfortran.so.3 (0x00002b098f00c000)
        libm.so.6 => /lib64/libm.so.6 (0x00002b098f331000)
        libgcc_s.so.1 => .../libgcc_s.so.1 (0x00002b098f5b4000)
        libquadmath.so.0 => .../libquadmath.so.0 (0x00002b098f7cb000)
        libc.so.6 => /lib64/libc.so.6 (0x00002b098fa07000)
        libpthread.so.0 => /lib64/libpthread.so.0 (0x00002b098fd60000)
        /lib64/ld-linux-x86-64.so.2 (0x0000003185e00000)
```

Looks much healthier! (I've shortened some of the library paths)

# Summary

I was able to install `numpy` by first building and installing OpenBlas to a non-standard location, and then
manually building `numpy` by creating the `site.cfg` file to point to the OpenBlas libraries
and specifying which Fortan compiler to use.





