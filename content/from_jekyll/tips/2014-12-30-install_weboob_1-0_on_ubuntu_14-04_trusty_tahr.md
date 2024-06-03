---
layout: post
title: Install Weboob 1.0 on Ubuntu 14.04 (Trusty Tahr)
categories:
 - tips
tags:
 - weboob
 - Ubuntu
image:
 feature: feature_image_green.png
comments: true
share: true
---

As stated on the Weboob [install page](http://weboob.org/install), Ubuntu packages for [Weboob](http://weboob.org/) are lagging behind (a lot). Package for the current LTS version of Ubuntu (14.04 - Trusty Tahr) is version 0.g-1 (can find how old this version is). The current version of Weboob (version 1.0, out October 2014) is packaged for Ubuntu 15.04 (Vivid Vervet).

So, here is how I installed from source the latest stable version of Weboob (1.0) on Ubuntu 14.04 (Trusty Tahr).


As stated on the website "Weboob is a collection of applications able to interact with websites, without requiring the user to open them in a browser. It also provides well-defined APIs to talk to websites lacking one". 

Personnaly, I use Weboob to access my bank website and retrieve my history and incoming operations data from the command line to process it.

# checkout Git source

create a Weboob directory:

{% highlight bash %}
sudo mkdir /opt/weboob
{% endhighlight %}

checkout Weboob stable sources :

{% highlight bash %}
$ mkdir /tmp/weboob
$ cd /tmp/weboob
$ git clone git://git.symlink.me/pub/weboob/stable.git src
{% endhighlight %}

# Install dependencies

## Python basics

Install Python 2.7

{% highlight bash %}
$ sudo apt-get install python2.7
{% endhighlight %}

Install setuptools

by hand (cf. [https://pypi.python.org/pypi/setuptools#unix-wget](https://pypi.python.org/pypi/setuptools#unix-wget)):

{% highlight bash %}
$ wget https://bootstrap.pypa.io/ez_setup.py -O - | sudo python
{% endhighlight %}

>note: I though for a minute that the `ez_setup.py` program was stuck but it turned out that the prompt for the sudo password was lost in the middle of noisy logs. So, if it happends to you, just it `enter`, you will be prompted for the sudo password again.

or with apt-get (not sure the version of setuptools is recent enough, though, I used the manual instal):

{% highlight bash %}
sudo apt-get install python-setuptools
{% endhighlight %}

## Dependencies for Weboob

Install dependencies for Weboob:

{% highlight bash %}
$ sudo apt-get install python-requests
{% endhighlight %}

## Dependencies for boobank

Currently, the only module I use is boobank, which has dependencies of its own:

{% highlight bash %}
$ sudo apt-get install python-dateutil python-prettytable python-mechanize python-cssselect
{% endhighlight %}

# Local install

We will do a local install of Weboob as the system install is discouraged on the [Weboob instal page](http://weboob.org/install).

Create `bin` directory in your home directory (if it does not exist yet). This is where we will be telling the local installation tool to create the Weboob executable:

{% highlight bash %}
$ mkdir ~/bin
{% endhighlight %}

and run the local installer:

{% highlight bash %}
$ cd /tmp/weboob/src
$ ./tools/local_install.sh ~/bin
{% endhighlight %}

# verify install

Add the `~/bin` directory to your PATH (if it not already), you can then just type `boobank`.

In the meantime, you can make sure the install directly by running:

{% highlight bash %}
$ ~/bin/boobank
{% endhighlight %}



