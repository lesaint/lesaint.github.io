---
layout: post
title: Creating a patch from a GIT commit
tags: git
---

Recently I had to create patch from a local commit to apply a totally different branch and on a different clone. Obviously I couldn't use `git cherry-pick` so I tried and found out to create a patch from a GIT commit.


It all comes down to using git format-patch command and the patch shell command : 

## create patch from last commit (local or not)

```sh
git format-patch -1 HEAD
# creates a patch file in the root directory of the GIT clone : lest say some_file.patch
```

## apply patch

```sh
patch -p1 < [path_to]/some_file.patch
```

source : [http://stackoverflow.com/questions/13192806/how-to-generate-a-git-patch-with-a-local-commit](http://stackoverflow.com/questions/13192806/how-to-generate-a-git-patch-with-a-local-commit)

