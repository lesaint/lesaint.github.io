title: Fix screen not working on QNAP
tags: Linux, QNAP


`screen` is a utility available on Linux that create virtual terminals.

In practice, it enables user to run command on a remote device (ie. typically via a SSH session) that will continue
running even if the connection is interrupted.

# Screen is broken on QNAP TS-253E

Unfortunately, by default (tested right after installation), `screen` doesn't work on QNAP systems (tested on QTS 5.0 and QTS 5.1).

When running `screen`, it fails with an error such as

```
# screen
/var/run/utmp: No such file or directory
Cannot find termcap entry for 'xterm-256color'
```

# Fix screen

Create the missing file and some symlinks.

```shell
touch /var/run/utmp
ln -s /usr/share/terminfo/x/xterm-xfree86 /usr/share/terminfo/x/xterm-256color
ln -s /usr/share/terminfo/x/xterm-xfree86 /usr/share/terminfo/x/xterm-color
```

[//]: # (## Make the change survive reboot)
[//]: # ()
[//]: # (The created file and symlinks will disappear upon reboot.)

## Alternative fix

Rather than create symlinks, one can make `screen` use existing termcap entry with the env variable `TERMINFO`.

```shell
TERMINFO='/usr/share/terminfo/' screen
```

However, this solution has proven more cumbersome and less reliable.

!!! note " Sources"

    * [screen man page](https://linux.die.net/man/1/screen)
    * [fix source](https://www.shan.info/item/451-screen-var-run-utmp-no-such-file-or-directory-cannot-find-termcap-entry-for.html)