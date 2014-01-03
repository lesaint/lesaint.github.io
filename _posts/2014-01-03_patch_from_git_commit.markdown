---
layout: post
title: Creating a patch from a GIT commit
tags: git
---

It all comes down to using git format-patch command and the patch shell command : 

1. create patch from last commit (local or not)

```shell
git format-patch -1 HEAD
# creates a patch file in the root directory of the GIT clone : lest say some_file.patch
```

2. apply patch

```shell
patch -p1 < [path_to]/some_file.patch
```


source : http://stackoverflow.com/questions/13192806/how-to-generate-a-git-patch-with-a-local-commit

