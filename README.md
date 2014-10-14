Lee Mendelowitz's blog
==============

Repo for managing the content and deployment of my [blog](https://leemendelowitz.github.io/blog/). This repo has a Makefile which will publish content to the gh-pages branch of this repo.

This I how I set everything up for myself. You can follow similar steps to get your own blog up and running.

## Install dependencies

```bash
sudo pip install pelican ghp-import markdown
```

## Set up remote

```bash
git remote add github git@github.com:LeeMendelowitz/blog.git
```

Only I have write access to this remote repo, but if you are setting up your own blog
simply replace my repo with yours!

# Add content

Add an article to the ```content``` directory.

## Generate the blog

The blog can be generated using the Makefile.

```bash
make html
```

This will store content in a directory called ```output```.

## Preview the blog
You can preview the blog locally by running the server and visiting [http://localhost:8000](http://localhost:8000).
```bash
make serve
```

## Publish to github
```bash
make github
```
Now checkout the [blog url](http://leemendelowitz.github.io/blog/).
