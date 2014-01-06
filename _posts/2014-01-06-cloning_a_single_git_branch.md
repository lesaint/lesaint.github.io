---
layout: post
title: Cloning a single branch
tags: git
---

When I get to checkout an existing repo which purpose is almost only to store binaries, I really would rather avoid cloning all the branches and tags locally because :
* I don't want to store all the useless old binaries
* I know I will use only one branch as a source and the futur ones
* I want to save space on my SSD

So I googled a little a found this tip : [http://stackoverflow.com/a/4146786](http://stackoverflow.com/a/4146786)

```sh
mkdir $BRANCH
cd $BRANCH
git init
git remote add -t $BRANCH -f origin $REMOTE_REPO
git checkout $BRANCH
```

This technic is a litle bit manual, but has many advantages :
* writing a shell script to automate it is only a few hits on the keyboard away
    - hay ! How hard would it be to create a new Git command ? I must find time to dig into that
    - maybe a simple GIT alias could do the job
* you don't get pushing problems as you can get when using git shallow cloning
* you really checking a single reference branch as opposed to using git clone -b option

```sh
git clone user@git-server:project_name.git -b branch_name
```

* checking out any branch/tag from the repo can be done by the regular git checkout command
    - one just need to know the name of the branch/tag from another source
* retrieving all the missing branches can be done in a single command

```sh
git fetch --all
```
