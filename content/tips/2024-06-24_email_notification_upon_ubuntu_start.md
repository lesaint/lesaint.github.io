title: Send email notification upon Ubuntu server restart
tags: Ubuntu

[TOC]

I want to be notified by email upon restart of the remote server serving the HDD where I do the offsite backup of my
data.

I used `init` in the past for such purpose, combined with a script that sends an email.

But `init` is gone and has been replaced by `systemd` in Ubuntu for a while now.

Yet, the same result can be achieved by creating a service in `systemd` and have it run only once.

# Send an email

I'll create a script in my home directory that sends me an email: `vi ~/scripts/notify_start.sh`.

To prevent emails from stacking in the same conversation in Gmail, I'll include the current date and time in the subject
(plus it's a useful information, in case emails are delayed).

Since restarts happen only so often, I'll include instructions in the body of what and how I should be doing manually
upon restart, in case I forget.

I'll use `ssmtp` to send the email, see [how to configure gmail with SSMTP on Ubuntu]({filename}/tips/2023-12-12_configure_ssmtp_with_gmail_on_ubuntu.md).

I'll use the braces + pipe trick and the `echo` command to send multiple lines to `ssmtp` (over the harder to read `cat`
+ delimiter, which I find harder to read and maintain).

```bash
#!/usr/bin/env bash

set -euo pipefail

DATE=$(date +"%Y-%m-%d-%H%M%S")
{
        echo "Subject: MyServer (re)started at $DATE"
        echo
        echo "This email is sent from systemd service notify_start.service on MyServer."
      echo "Check service logs with either 'sudo systemctl status notify_start.service' or 'journalctl -u notify_start.service'."
        echo "" 
        echo "Immediate actions to take:"
        echo " * mount and open HDD with '/blablabla/mount.sh'"
} | ssmtp me@gmail.com
```

# Create the service

The unit of work in `systemd` is a `unit`. We will use one of type `service`, since `systemd` starts, stops and 
generally manages the lifecycle of those, and we can declare dependencies on other services (see below).

A unit is created with a configuration file. I'll use `/etc/systemd/system` as location since it prevails over any other
and I have root access.

`sudo vi /etc/systemd/system/notify_start.service`

* I create and a description to the unit
    ```
    [Unit]
    Description=Send me an email when system starts
    ```
* the unit is a service
    ```
    [Service]
    ``` 
* the service calls the above script (upon starting):
    ```
    ExecStart=/home/phan/scripts/pidatabak_scripts/notify_start/notify_start.sh
    ```
* the service must be started only once (to run the script only once):
    ```
    Type=oneshot
    ```
* since the script sends an email, the service requires network to be available before running:
    ```
    After=network-online.target
    Wants=network-online.target
    ```

Side benefit: since the service just calls a script, it can be easily duplicated to serve other purpose.

# Test the service

After testing the script, test the service with `sudo systemctl start notify_start.service`.

If service was already tested, stop it first: `sudo systemctl stop notify_start.service`.

# Enable the service

To have the service managed by `systemd`, it needs to be enabled with `sudo systemctl enable notify_start.service`.

This fails with the following message:

```
The unit files have no installation config (WantedBy=, RequiredBy=, Also=,
Alias= settings in the [Install] section, and DefaultInstance= for template
units). This means they are not meant to be enabled using systemctl.

Possible reasons for having this kind of units are:
• A unit may be statically enabled by being symlinked from another unit's
  .wants/ or .requires/ directory.
• A unit's purpose may be to act as a helper for some other unit which has
  a requirement dependency on it.
• A unit may be started when needed via activation (socket, path, timer,
  D-Bus, udev, scripted systemctl call, ...).
• In case of template units, the unit is meant to be enabled with some
  instance name specified.
```

To fix this, add the following:

```
[Install]
WantedBy=multi-user.target
```

# Monitor the service

* check logs with either `sudo systemctl status notify_start.service` or `journalctl -u notify_start.service`
* check status with `sudo systemctl status notify_start.service`


```
[Unit]
Description=Send me an email when system starts
# source: https://systemd.io/NETWORK_ONLINE/
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/home/phan/scripts/pidatabak_scripts/notify_start/notify_start.sh

[Install]
WantedBy=multi-user.target
```

!!! note " Sources"
    * [Fixing missing WantedBy](https://unix.stackexchange.com/a/506374)
    * [Understanding Systemd Units and Unit Files](https://www.digitalocean.com/community/tutorials/understanding-systemd-units-and-unit-files)