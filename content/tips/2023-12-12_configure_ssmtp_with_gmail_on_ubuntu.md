title: Configure sSMTP with Gmail on Ubuntu
tags: Ubuntu

`sSMTP` is a send-only `sendmail` emulator for Linux. It replaces `sendmail`, in place, but implements only send features.

# Create an App password in Gmail

**Only required when Two-Factor-Authentication (2FA) is enabled**, but:

1. everyone should have 2FA enabled
2. prevents storing the email's password in plain text configuration files

Procedure:

* go to `Google Account` > `Security` > `2-Step verification`
* scroll to the bottom to `App passwords`

# Install ssmtp

```shell
sudo apt install ssmtp
```

Configure `sSMTP`, edit `/etc/ssmtp/ssmtp.conf`:

```
#
# Config file for sSMTP sendmail
#
# The person who gets all mail for userids < 1000
# Make this empty to disable rewriting.
root=postmaster

# The place where the mail goes. The actual machine name is required no 
# MX records are consulted. Commonly mailhosts are named mail.domain.com
mailhub=mail

# Where will the mail seem to come from?
#rewriteDomain=

# The full hostname
hostname=Acme

# Are users allowed to set their own From: address?
# YES - Allow the user to specify their own From: address
# NO - Use the system generated From: address
#FromLineOverride=YES

# added by me below
AuthUser=acme@gmail.com
AuthPass=secret_application_password
mailhub=smtp.gmail.com:587
UseSTARTTLS=YES
FROM:acme@gmail.com
```

# make a test


```shell
{ echo "Subject: test's subject"; echo; echo "This is another test"; } | ssmtp donut@gmail.com
```

!!! note " Sources"

    * [Sending Email through Google from the Command Line](https://nextpertise.net/posts/230313_command_line_email/)
    * [You can Still use Gmail SMTP to Send E-Mails in 2024 and Here's How](https://noted.lol/setup-gmail-smtp-sending-2023/)
    * [Oneliner to test `sSMTP`](https://unix.stackexchange.com/a/244296)
