Title: Finding files with GNU find!
Date: 2016-12-16
Slug: gnu-find
Author: Lee Mendelowitz
Tags: Linux
Summary: How to use GNU find to find files.

If you want to learn how to use your computer like a boss, it's a good idea
to get comfortable working on the command line <a href="http://linuxcommand.org/lc3_learning_the_shell.php" target="_blank">with a shell</a>. Oftentimes it's a more effective way to get certain things done.

If you are on MacOS or Linux, you probably already have the `bash` shell installed. Limited `bash` support was added to Windows in Windows 10. Once you are comfortable working in the shell you'll want to learn to use command line
utilities like `find`, `xargs`, `grep` (and much more) to get stuff done and make your day to day computing life easy.

There are so many practical applications of these utilities. In this post, I'll introduce `find` which is a utility for finding files based on criteria like name, file size, or the timestamp when the file was created or last accessed or modified. In 

Let's say I've got a bunch of files in a folder, and I want to copy some (but not all) of the files to Dropbox. I only want to copy image files that have been created in the last week. We will explore the use of command line tools to get this job done.

### Using `ls` to list files by extension

The `ls` utility can be used to list the files in the current directory:

```bash
ls -1 *.jpg
```

This works well in simple situations, but it's not the most robust solution. What if some files have the extension '.JPG' or '.jpeg' or '.png'? And how do we only list some files based on creation time? `ls` cannot handle these situations.

### Using `find` to list files by extensions

The `find` utility can be used to find files based on various search criteria. To filter files by name pattern, ignoring case:

```bash
find . -iname '*.jpg'
```

This means "find in this directory or the subdirectories contained therein
any file that has an extension .jpg, case insensitive." You can use `-name` for case sensitive searches.

Note the quotes around the pattern: '*.jpg'. We must use quotes to prevent the shell from performing <a href="http://linuxcommand.org/lc3_lts0080.php" target="_blank">shell expansion</a>.


### Multiple Criteria

To accommodate multiple possible extensions, we must add arguments to
`find`,

By default, each criteria provided to `find` is added using AND logic (i.e. all the listed criteria must be true for a file to match). Here we must use `-o` to add criteria using OR logic, where a file must match only some of the search criteria.


```bash
find .  \
 -iname '*.jpg' \
 -o -iname '*.jpeg' \
 -o -iname '*.png'
```

This means "find in this directory or the subdirectories contained therein
any file that has an extension '.jpg', or '.jpeg' or '.png', case insensitive".

If you forgot the `-o` flags then `find` would come up empty because file names cannot end in '.jpg' AND '.jpeg'.

### Using maxdepth 

We can make this search even more robust by requiring the file be a regular file (i.e. not a directory) and the results be in the current working directory, but not a subdirectory. 

The argument `-maxdepth 1` says look in this folder, but not any deeper. The argument `-type f` means look for regular files, but not directories.

To get the OR logic to work right, we need to group our file name criteria in the matching parentheses `\(` and `\)`. The parentheses must be escaped with the backlash (common practice when working on the command line. (Sometimes you gotta escape stuff.)

```bash
find .  \
 -maxdepth 1 \
 -type f \
 \( \
     -iname '*.jpg' \
     -o -iname '*.jpeg' \
     -o -iname '*.png' \
 \)
```

### Using `-ctime` for creation time

We use the `-ctime` argument to find files based on file creation time. To find created in the last 7 days, we use `-ctime -7`

```bash
find .  \
 -maxdepth 1 \
 -type f \
 -ctime -7 \
 \( \
     -iname '*.jpg' \
     -o -iname '*.jpeg' \
     -o -iname '*.png' \
 \) 
```

### Using `find` + `xargs`

Alright, we are novice experts at finding files now. I want to find files and do something with those files I find - like move them to Dropbox.

Since I've installed Dropbox on my MacBook, if I copy files into `~/Dropbox` the Dropbox app will sync them to the Dropbox service. We can use the `xargs` utility to do the heavy lifting.

`xargs` is processor of sorts: for each argument in its input, it runs a program and constructs the command line argumants passed to that program.

For example, I effectively want to do something like this:

```bash
cp photo1.jpg ~/Dropbox
cp photo2.jpg ~/Dropbox
cp photo3.jpg ~/Dropbox
```
etc., but 100 times. or 1000 times, once for each photo. This is a job for `xargs`. You can pass the results of `find` into `xargs` using the pipe operator `|`, as so:

```bash
find .  \
 -maxdepth 1 \
 -type f \
 -ctime -7 \
 \( \
     -iname '*.jpg' \
     -o -iname '*.jpeg' \
     -o -iname '*.png' \
 \) \
 | xargs -I {} cp {} ~/Dropbox
```

For each file returned by `find` (photo1.jpg, photo2.jpg, etc.), `xargs` will run `cp {} ~/Dropbox` where the placeholder `{}` is replaced by the arguments. 

There is one gotcha - sometimes filenames have spaces (boooo!). This can create a problem for this `find` into `xargs` pipeline. The solution is to instruct `find` to separate results with a null character, and then have `xargs` parse it's input list of arguments using this separator. We use `-print0` argument with `find`, and `-0` with xargs:

```bash
find . \
 -maxdepth 1 \
 -type f \
 -ctime -7 \
 \( \
     -iname '*.jpg' \
     -o -iname '*.jpeg' \
     -o -iname '*.png' \
 \) \
 -print0 \
 | xargs -0 -I {} cp {} ~/Dropbox
```

`-print0` must come at the end, after the search criteria.

Alright good stuff. This is nice, powerful, and flexible!

## Other arguments to find

### File size

Use '-size' to search based on file size. Here's a way to search for large files over 100 MB in your home directory:

```bash
find ~ -type f -size +100M
```

use `k` for kilobytes, 'M' for Megbytes, `G` for gigabytes.


### Timestamps in depth

Use `-ctime`, `-mtime`, `-atime` to find files that have been created, modified, accessed n days ago. There are some rounding affects, where fractional parts of days are ignored. Check out the manpage (`man find`) for more information. Here are some quick examples:

To find files modified between 1 and 2 days ago, supply argument `-mtime 1`.

```bash
find . -mtime 1
```

Since the fractional part of days are ignored, files modified 1.001 days and 1.999 days ago both match `-mtime 1` exactly.

To find files modified less than 1 days ago:

```bash
find . -mtime -1
```

Find files modified more than 1 days ago:

```bash
find . -mtime +1
```

Notice how the `+` and `-` affect the search. Like all of the `find` criteria, you can combine them. For example:

```bash
find . -mtime +0 -mtime -2
```

means find files that have modified 1 or more days ago (`-mtime +0`) **and** less than 2 days ago (`-mtime -2`). This is the same as `find . -mtime 1`.

Use `-cmin`, `-mmin`, `-amin` to find files that have been created, modified, accessed n minutes ago. This works just like the examples above, accept where n represents minutes instead of days.

## Conclusion

`find` is a very useful utility for finding files. It works great with `xargs`, for running additional commands for every file that matches your search criteria.

