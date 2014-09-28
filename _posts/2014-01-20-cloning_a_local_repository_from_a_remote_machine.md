---
layout: post
title: Cloning a local Git repository from a remote machine
tags: Git SSH
categories: articles
image:
 feature: feature_image_green.png
redirect_from:
  - /2014/01/20/cloning_a_local_repository_from_a_remote_machine.html
comments: true
---

If you happen to have a Git repository cloned a machine (let's say machine@work) and you want to retrieve it on another machine (let's say machine@home),
you have a better (as in faster and more efficient) option than `scp` or `rsync` : `git clone`.


# Git clone of a local repository over SSH

Obviously, you could clone from the same remote repository (let's say Remote) as machine@work, but you may have local branches on machine@work that you specificall want to work on.
Pushing local branche from machine@work to Remote is an option but it could polute other developers clones and/or you may not have access to Remote from machine@home.

Let's say the clone on machine @work is in directory `~/DEV/myclone`, here are the commands to use :

```sh
cd ~/STUFF_FROM_WORK/
git clone lesaint@lesaint.work.com:~/DEV/myclone/
```

And that's it !

>Please note :
> 
> * you might be prompted to enter a password to connect over ssh (unless you have a ssh-agent with a loaded key for machine@work)
> * you can specify the path where to clone the repository by adding a third argument like any other clone command
>    - `git clone lesaint@lesaint.work.com:~/DEV/myclone/ local_clone_name`
> * I used the "scp style" syntaxe of the `git clone` argument
>   - the ssh style syntax would be `ssh://lesaint@lesaint.work.com/~/DEV/myclone/`

# Changing remote from machine to the true remote

After cloning from machine @work, you might notice that the remote of the clone of machine @home is machine @work.

To fix that in the event you would happen to access to remote from home and that you would like to push to remote directly :

```sh
cd ~/STUFF_FROM_WORK/myclone
git remote set origin lesaint@gitserver.work.com:project.git
```
