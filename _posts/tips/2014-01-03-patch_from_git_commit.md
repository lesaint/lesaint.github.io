---
layout: post
title: Creating a patch from a GIT commit
tags:
 - Git
categories:
 - tips
image:
 feature: feature_image_green.png
redirect_from:
  - /2014/01/03/patch_from_git_commit.html
  - /articles/2014/01/03/patch_from_git_commit.html
comments: true
---

Recently I had to create patch from a local commit to apply a totally different branch and on a different clone. Obviously I couldn't use `git cherry-pick` so I tried and found out to create a patch from a GIT commit.


It all comes down to using git format-patch command and the patch shell command : 

## create patch from last commit (local or not)

{% highlight sh %}
git format-patch -1 HEAD
# creates a patch file in the root directory of the GIT clone : lest say some_file.patch
{% endhighlight %}

## apply patch

{% highlight sh %}
patch -p1 < [path_to]/some_file.patch
{% endhighlight %}

source : [http://stackoverflow.com/questions/13192806/how-to-generate-a-git-patch-with-a-local-commit](http://stackoverflow.com/questions/13192806/how-to-generate-a-git-patch-with-a-local-commit)

