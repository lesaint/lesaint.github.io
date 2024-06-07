Title: Cloning a single branch
Tags: Git

On this new project I'm working one, there is this huge repository that serves as a deployment mean for binaries in the stage and production environnement.

Most branches content is totally different from one another and no one cares about the old branches and rarely use the tags.

Since my SSD was almost full, I wanted to avoid cloning the whole repository and clone only a specific branch instead. I would later retrieve other branches (and tags, very rarely) one by one.

Using the `-t` option of `git remote` and a serie of commands, we can achieve that.


### Cloning a single branch
To clone a repository and retrieve a single branch can be done as follow :

!!! note " Sources"

    * [http://stackoverflow.com/a/4146786]()

```sh
# create clone directory
mkdir $REPO
cd $REPO
# create an empty local master branch
git init
# add a remote repository for a specific branch
git remote add -t $BRANCH -f origin $REMOTE_REPO
# retrieve remote branch on disk
git fetch
# checkout branch locally
git checkout $BRANCH
```

### Checkout new branches

Checking out any branch/tag from the repo can be done as follow :
It indeed requires to know the name of the remote branch from another source than your local checkout.

```sh
cd $REPO
# add a new remote branch
git remote set-branches --add origin $NEW_BRANCH
# fetch all remote branches (the new one included) to disk
git fetch
# checkout branch locally
git co $NEW_BRANCH
```

If the added remote branche does not exist on the remote repository, you will get the following error, fetch will fail.

```sh
fatal: Couldn't find remote ref refs/heads/WRONG_BRANCH
fatal: The remote end hung up unexpectedly
```

The problem is that your local repository get kind of corrupted and all the next `git fetch` command will also fail with the same error.

To fix it, edit file `.git/config` and remove the wrong entry under '[remote origin]' starting with `fetch =`.

!!! note " Sources"

    * [http://stackoverflow.com/questions/6930147/git-pull-displays-fatal-couldnt-find-remote-ref-refs-heads-xxxx-and-hangs-up#comment8276807_6930399]()

### Discussion
This technic is a litle bit manual, but has many advantages :

* writing a shell script to automate it is only a few hits on the keyboard away
    - hay ! How hard would it be to create a new Git command ? I must find time to dig into that
    - maybe a simple GIT alias could do the job
* you don't get pushing problems as you can get when using git shallow cloning
* you really are checking a single reference branch as opposed to using `git clone -b option`

```sh
# retrieves all the remote branches locally and then checkout branch_name
git clone user@git-server:project_name.git -b branch_name
```
