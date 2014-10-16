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
---

To install the Google Cloud SDK, you can follow the [installation guidelines](https://cloud.google.com/sdk/) available online. But if you are running Ubuntu and uses Oh-My-Zsh (or to some extent, Zsh alone), automatic installation won't work and you need to do some manually.


## Install via the bash installer

Run the following command to download and install the SDK on your disk.

```sh
curl https://sdk.cloud.google.com | bash
```

### Bash

If your are running ```bash```, answer ```Y``` when prompted to add ```gcloud``` to the ```PATH``` and install auto-completion. Don't worry, the installer creates a backup before modifying your ```.bashrc```.

### Zsh

If you are running ```Zsh```, specify the path to your ```.zshrc``` when prompted instead of going for the default ```.bashrc``` file.

You will then have to manually modify your ```.zshrc```.

The installer adds the following lines:

```sh
# The next line updates PATH for the Google Cloud SDK.
source '/path/to/google-cloud-sdk/path.bash.inc'

# The next line enables bash completion for gcloud.
source '/path/to/google-cloud-sdk/completion.bash.inc'
```

Just replace the ```bash``` part in the file names with ```zsh``` to use the Zsh specific scripts provided with the SDK.

### Oh-my-zsh compatibility

I'm running using Oh-My-Zsh and unfortunately, the procedure above did not work for me.

When loading a new shell, I got errors such as the following and command line completion did not work.

```sh
/path/to/google-cloud-sdk/completion.bash.inc:8: command not found: complete
/path/to/google-cloud-sdk/completion.bash.inc:19: parse error near `]]'
```

I believe these errors are related to me using Oh-My-Zsh or specific to my installation. Anyway, I did the following to fix the install.

#### Install gcloud-zsh-completion

gcloud-zsh-completion provides awesom completion for ```gcloud``` command line.

Clone the [gcloud-zsh-completion repository](https://github.com/littleq0903/gcloud-zsh-completion) somewhere on disk. 

```sh
git clone https://github.com/littleq0903/gcloud-zsh-completion.git
```

#### modify .zshrc

Add the following lines to your ```.zshrc``` __before__ the line where oh-my-zsh is loaded (```source $ZSH/oh-my-zsh.sh```).

Personnaly, I have put them at the beginning of my ```.zshrc```.

```sh
# Google Cloud SDK
source '/path/to/google-cloud-sdk/path.zsh.inc'

# load Google Clound SDK completion for Zsh by Colin Su (LittleQ -- https://github.com/littleq0903/gcloud-zsh-completion)
fpath=(/path/to/gcloud-zsh-completion/src $fpath)
autoload -U compinit compdef
compinit
```
