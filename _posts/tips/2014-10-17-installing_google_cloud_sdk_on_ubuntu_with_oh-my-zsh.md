---
layout: post
title: "Installing Google Cloud SDK on Ubuntu with Oh-My-Zsh"
tags:
 - Cloud
 - Google Cloud
 - Ubuntu
 - Oh-My-Zsh
categories:
 - Tips
image:
 feature: feature_image_green.png
comments: true
share: true
---

To install the Google Cloud SDK, you can follow the [installation guidelines](https://cloud.google.com/sdk/) available online. But if you are running Ubuntu and uses Oh-My-Zsh (or to some extent, Zsh alone), automatic installation won't work and you need to do some manual steps.


## Install via the bash installer

Run the following command to download and install the SDK on your disk.

{% highlight sh %}
curl https://sdk.cloud.google.com | bash
{% endhighlight %}

### Bash

If your are running ```bash```, answer ```Y``` when prompted to add ```gcloud``` to the ```PATH``` and install auto-completion. Don't worry, the installer creates a backup before modifying your ```.bashrc```.

### Zsh

If you are running ```Zsh```, specify the path to your ```.zshrc``` when prompted instead of going for the default ```.bashrc``` file.

You will then have to manually modify your ```.zshrc```.

The installer adds the following lines:

{% highlight sh %}
# The next line updates PATH for the Google Cloud SDK.
source '/path/to/google-cloud-sdk/path.bash.inc'

# The next line enables bash completion for gcloud.
source '/path/to/google-cloud-sdk/completion.bash.inc'
{% endhighlight %}

Just replace the ```bash``` part in the file names with ```zsh``` to use the Zsh specific scripts provided with the SDK.

### Oh-my-zsh compatibility

I use Oh-My-Zsh as a shell and unfortunately, the procedure above did not work for me.

When loading a new shell, I got errors such as the following and command line completion did not work.

{% highlight sh %}
/path/to/google-cloud-sdk/completion.bash.inc:8: command not found: complete
/path/to/google-cloud-sdk/completion.bash.inc:19: parse error near `]]'
{% endhighlight %}

I did the following to fix the install.

#### load the SDK files before `Oh-My-Zsh`

First, move the lines added by the installer _before_ the source command loading `Oh-My-Zsh` (```source $ZSH/oh-my-zsh.sh```).

#### load missing `Zsh` module

Then two lines to tell `Zsh` to load and init some specific modules required for completion to work _before_ the `source` command for completion. I a no expert with `Zsh` nor `Oh-My-Zsh`, but looking at `oh-my-zsh.sh` it seems that only `compinit` is loaded.

You should end up with the following, at the beginning of your `.zshrc`.

{% highlight sh %}
# The next line updates PATH for the Google Cloud SDK.
source '/home/lesaint/GOOGLE_CLOUD/google-cloud-sdk/path.zsh.inc'

# The next lines enables bash completion in Zsh for gcloud. 
autoload -U compinit compdef
compinit
source '/home/lesaint/GOOGLE_CLOUD/google-cloud-sdk/completion.zsh.inc'
{% endhighlight %}
