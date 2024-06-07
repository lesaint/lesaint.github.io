title: Configure sSMTP with Gmail on Qnap
tags: Qnap

`sSMTP` is a send-only `sendmail` emulator for Linux. It replaces `sendmail`, in place, but implements only send features.

# Install and configure sSMTP

On QTS 5.X, `sSMTP` is already installed.

However, it is not the standard `ssmtp` binary: 

1. it doesn't support providing recipient as argument (ie. the standard `sendmail foo@bar.net`). Recipients must be provided as header in the message:
	```
	To: jane.doe@gmail.com
	Subject: This is a subject

	Did you receive this message?
	```
2. the configuration file is not in standard location (`/etc/ssmtp/ssmtp.conf`): `/etc/config/ssmtp/ssmtp.conf` 


# Configure sSMTP

Use the UI and Qnap's Notification center interface, add an email.

![clicks in QTS UI to create email account]({static}/images/2023-12-14_configure_ssmtp_with_gmail_on_qnap/screenshot_config_ssmtp_in_qnap.jpg)

!!! hint ""

	Qnap's QTS configures authentication with Gmail through Oauth token-based authentication.
	
	This can't be achieved (to my knowledge) in command line, but this is more secure than an Application Password
	stored in plain text (see [Configure sSMTP with Gmail on Ubuntu]({filename}/tips/2023-12-12_configure_ssmtp_with_gmail_on_ubuntu.md)).


!!! note " Sources"

    * [sSMTP man 8 page](https://linux.die.net/man/8/sendmail.sendmail)
	* [QTS 5.1.X documentation: Configuring an email notification server](https://docs.qnap.com/operating-system/qts/5.1.x/en-us/configuring-an-email-notification-server-EB4E6D7F.html)