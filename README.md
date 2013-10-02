LeeMendelowitz/github.io-blog
==============

Repo for managing the content and deployment of the blog LeeMendelowitz.github.io. This repo has a Makefile which will push to the LeeMendelowitz/LeeMendelowitz.github.io.git repo.

## Install dependencies

```bash
sudo pip install pelican
sudo pip install ghp-import
```

## Set up remote

Set up a remote called "blog" in the local repo for the blog's remote repo, which is hosted on Github at LeeMendelowitz/LeeMendelowitz.github.io.git.

```bash
git remote add blog	git@github.com:LeeMendelowitz/LeeMendelowitz.github.io.git
```

## Generate the blog

The blog can be generated using the Makefile.

```bash
make html
```

## Preview the blog
You can preview the blog locally by running the server and visiting http://localhost:8000.
```bash
make serve
```

## Publish to github
```bash
make github
```
