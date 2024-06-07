title: Emulate Crontab mailto feature with a script on Qnap NAS
tags: Bash, Linux, Qnap

[TOC]

I run jobs on a regular basis on my Qnap NAS with `cron` and I want to be notified if any of these jobs fails or sends
warnings.

`Crontab` has a simple and super neat feature called `MAILTO`.

When this variable is set, `Crontab` sends any output from the cron job to the recipient.

The variable is set by default and the recipient is the current user (owner) of the crontab and the mail is a Linux "in-"mail.

To disable the feature, set the variable to an empty value: `MAILTO=""`

!!! note " Sources"

    * [crontab man7 page](https://man7.org/linux/man-pages/man5/crontab.5.html)

# Crontab MAILTO not working on Qnap systems

Unfortunately, on Qnap NAS systems (at least on mine with QTS 5.X), `Crontab` `MAILTO` is disabled, not implemented, or
not working.

To work around this, one can write a Bash script that will mimic the behavior: call a command, and if anything is
written to `stdout` or `stderr`, send it by email to some recipient. 

!!! note " Sources"

    * [Qnap forum on Crontab not sending email](https://forum.qnap.com/viewtopic.php?p=718601&sid=1238e70ddd95a7f07639632eed6c758d)


# A script mimicking Crontab's MAILTO

## Requirements

1. `ssmtp` available on path and configured to send out emails

For tips on installing and configuring `sSMTP`, see [Configure sSMTP with Gmail on Ubuntu]({filename}/tips/2023-12-12_configure_ssmtp_with_gmail_on_ubuntu.md)
and [Configure sSMTP with Gmail on Qnap]({filename}/tips/2023-12-14_configure_ssmtp_with_gmail_on_qnap.md).

## Features

* sends an email if command has any output (either `stdout` or `stderr` or both) **and/or** exit code is non-zero
* otherwise, the script only executes the command and has no side effect
* subject is truncated to 78 chars
* subject contains the current user to identify who's crontab was executed
* subject contains the date and time of the execution of the command
	* this serves both a debugging purpose and prevents Gmail from not sending/receiving identical emails

!!! note " Sources"

    * [RFC 2822 recommendation on subject size](https://stackoverflow.com/a/1592310)

## How to use

In a `crontab` file, simply pass the command to execute as argument (**mind using quotes to avoid command be executed and/or part of it missing**):

```shell
[CRONEXPRESSION] /home/foo/scripts/cronmail.sh "/home/foo/scripts/bar.sh"
```

### send email only upon error output

Silence stdout with `1>/dev/null`, eg.:

```shell
[CRONEXPRESSION] /home/foo/scripts/cronmail.sh "/home/foo/scripts/bar.sh 1>/dev/null"
```

## The script

```shell
#!/bin/bash

# -----------------------------------------------------------------------------
# Bash unofficial strict mode [source](http://redsymbol.net/articles/unofficial-bash-strict-mode/)
# -----------------------------------------------------------------------------
set -euo pipefail
IFS=$'\n\t'

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------
fn_terminate_script() {
    if [ "${STDOUT:-}" != "" ]; then
        rm -f "$STDOUT"
    fi
}

fn_echo_email_header() {
    # email subject:
    #  * includes the date and time to work around Gmail not sending/receiving emails that are exactly the same
    #    (maybe this applies only over some period of time)
    #  * will be truncated to 78 chars (RFC 2822 recommendation [source](https://stackoverflow.com/a/1592310))
    local subject="[CRON][$USER][$CMD_DATE] ${CMD}"

    echo "To: $MAILTO"
    echo "Subject: ${subject:0:78}"
    echo ""
    echo "============ executed command ============"
    echo "$CMD"
    echo "============== return code ==============="
    echo "$CMD_RETURN_CODE"
}

fn_echo_email_no_output() {
    fn_echo_email_header
    fn_echo_email_footer
}

fn_echo_email_with_output() {
    fn_echo_email_header
    echo "================ output =================="
    cat "$STDOUT"
    fn_echo_email_footer
}

fn_echo_email_footer() {
    echo "=========================================="
}

fn_send_email() {
    ssmtp
}

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
# constants
MAILTO="foo.bar.acme@gmail.com"

# the command to execute from CRON
CMD="$1"
CMD_DATE=$(date +"%Y-%m-%d-%H%M%S")

# create temporary file to collect stdout and stderr to
STDOUT="$(mktemp /tmp/cronme.out.XXXXXXXXXX)" || (>&2 echo "failed to create temp file" && exit 1)

# ensure no file is left behind even if script is interrupted/killed
trap 'fn_terminate_script' SIGINT

# evaluate the command, capturing both stdout and stderr to a file
# disable bash's "e" option to ensure this script keeps on running if evaluated command is killed/exits with non-zero code
set +e
eval "$CMD" 1>"$STDOUT" 2>&1
CMD_RETURN_CODE=$?
set -e

if [ -s "$STDOUT" ]; then
    fn_echo_email_with_output | fn_send_email
elif [ $CMD_RETURN_CODE -ne 0 ]; then
    fn_echo_email_no_output | fn_send_email
fi

# clean up
fn_terminate_script
```
