Lee Mendelowitz's blog
==============

Repo for managing the content and deployment of my [blog](https://leemendelowitz.github.io/blog/). This repo has a Makefile which will publish content to the gh-pages branch of this repo.

This I how I set everything up for myself. You can follow similar steps to get your own blog up and running.

## Install dependencies

```bash
pip install pelican ghp-import markdown
```

## Clone the repository

```bash
git clone https://github.com/LeeMendelowitz/blog.git blog
cd blog
git submodule init
git submodule update
```

## Add content

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

## Publish to GitHub Pages

These instructions are if you want to publish the blog to [GitHub Pages](https://pages.github.com/).
This requires that you first create a GitHub repo to host the blog. Then modify the GitHub repo settings
to use GitHub pages.

### Set up remote

Once you have your GitHub repo to publish to, add your GitHub repo as a remote.
Call the remote "github". (Replace the URL below with the URL for your repo!)

```bash
git remote add github git@github.com:LeeMendelowitz/blog.git
```

Call the remote `github` as this is the name of the remote where the Makefile will try
to publish.

To publish to the `gh-pages` branch of your GitHub repo:

```bash
make github
```

Now checkout your public [blog url](https://leemendelowitz.github.io/blog/)!


