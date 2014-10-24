#!/usr/bin/env
#
# Code to compare the ls command on MAC OS X using the default and GNU ls.
# GNU ls was installed with hombrew:
#
# 'brew install coreutils'
# 
# Src:
# http://www.topbug.net/blog/2013/04/14/install-and-use-gnu-command-line-tools-in-mac-os-x/
#
#
# Weird irreproducible behavior. I think GNU ls performs better on first run than
# default ls, but can't reproduce consistently.
#
import os, shlex, subprocess
from subprocess import PIPE
import timeit
from datetime import datetime

DEVNULL = open(os.devnull, 'wb')

def get_stdout(cmd):
  if isinstance(cmd, str):
    cmd = shlex.split(cmd)
  p = subprocess.Popen(cmd, stdout=PIPE)
  sout, serr = p.communicate()
  return sout.strip()

HOME = os.path.expanduser("~")
DOWNLOADS = os.path.join(HOME, "Downloads")
os.chdir(DOWNLOADS)
BREW_PFX = get_stdout("brew --prefix")

cmd1 = shlex.split("/bin/ls -l")
cmd2 = shlex.split(os.path.join(BREW_PFX, 'bin', 'gls') + ' -l')

def simple_time(cmd):
  s = datetime.now()
  p = subprocess.call(cmd1, stdout = DEVNULL, stderr = DEVNULL)
  e = datetime.now()
  return (e-s).total_seconds()

# p1 = subprocess.call(cmd1, stdout = DEVNULL, stderr = DEVNULL)
# p2 = subprocess.call(cmd2, stdout = DEVNULL, stderr = DEVNULL)

print simple_time(cmd1)
print simple_time(cmd2)
