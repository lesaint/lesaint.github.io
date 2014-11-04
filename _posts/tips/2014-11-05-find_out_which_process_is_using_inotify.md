---
layout: post
title: "Find out which process is using Inotify"
tags:
 - Linux
categories:
 - tips
image:
 feature: feature_image_green.png
---

Here is how to list processes which are using Inotify to watch FileSystem changes under Linux and also list how many Inotify nodes each one is using.

This can come in handy when you want to make sure some process (such as `jekyll` with Auto-regeneration enabled) is actually using Inotify or to find out if your are about to run out of Inotify nodes because a process is creating too much of them.


# List processes

For each Inotify node used by a process, a file descriptor is created in the file descriptor directory of the process in `/proc`.

Use the following command to list the processes with at least one Inotify node.

```sh
ps $(find /proc/*/fd/* -type l -lname 'anon_inode:inotify' 2>/dev/null | sed 's+/proc/\([^/]*\)/fd/.*+\1+')
```

The result is something like the following:

```sh
  PID TTY      STAT   TIME COMMAND
 2244 ?        Sl     0:03 /usr/lib/gnome-settings-daemon/gnome-settings-daemon
 2294 ?        Sl     3:22 compiz
 2300 ?        Sl     0:01 nautilus -n
 2325 ?        S      0:00 /usr/lib/gvfs/gvfs-gdu-volume-monitor
 2820 ?        Rl     0:16 gnome-terminal
 3081 ?        Sl     0:00 gnome-screensaver
 3543 ?        Sl     0:00 update-notifier
13246 ?        Sl     0:06 /opt/sublimetext/sublime/sublime_text
14053 pts/3    Sl+    0:18 ruby2.1 /usr/local/bin/jekyll serve -w --draft
```

You can get more details about the process using the regular `ps` options such as `-f`;


```sh
ps -f $(find /proc/*/fd/* -type l -lname 'anon_inode:inotify' 2>/dev/null | sed 's+/proc/\([^/]*\)/fd/.*+\1+')
```

>source: https://bbs.archlinux.org/viewtopic.php?pid=1340024#p1340024

# Count nodes per process

```sh
find /proc/*/fd/* -type l -lname 'anon_inode:inotify' -print
```

Result will look like the following:

```sh
/proc/13246/fd/11
/proc/13246/fd/12
/proc/14053/fd/8
/proc/2232/fd/5
/proc/2244/fd/11
```

The first number on each line is the process id, the second number is the number of nodes for this process.

>source: http://unix.stackexchange.com/questions/15509/whos-consuming-my-inotify-resources#comment21001_15549
