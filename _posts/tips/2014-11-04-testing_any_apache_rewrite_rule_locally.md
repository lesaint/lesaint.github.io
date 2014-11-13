---
layout: post
title: "Testing any Apache rewrite rule locally"
tags:
 - Apache
 - Ubuntu
 - Testing
categories:
 - tips
image:
 feature: feature_image_green.png
comments: true
---

Recently, I had to write a bunch of Apache rewrite rules which applied to the whole URL, including the hostname. I also add to use `RewriteMap` for efficiency.

I initially though this would be difficult to test locally but, in fact, with little modifications of a local Apache instance and use of the `/etc/hosts` file, it's pretty easy.

This article will detail how I did it on my computer running Ubuntu and hopefully it will help others setup their own computer.


* Table of Contents
{:toc}

# Testing rewrite rules

## online

Online tools such as [htaccess tester](http://htaccess.madewithlove.be/) exists and can come in handy to test simple rules but that are limited techically (they usually advertise their limitations) but also by design: e.g. they can not support [RewriteMap](http://httpd.apache.org/docs/current/en/mod/mod_rewrite.html#rewritemap).

> when working rules, [regex101.com](http://regex101.com/#pcre) is pretty usefull to test regular expressions. Be sure to be in "pcre" mode as this is the intepretor used by Apache.

## locally

Testing locally is the only way to fully test the rewrite rules you write, you can even test various version of Apache (but I won't cover that here).

Fortunatly, it is not so complicated to set up a local instance to test even host-based rewrite rules.

# Installing and configuring Apache

## install

If you already have Apache installed, skip this.

Installation under Ubuntu is trivial:

{% highlight sh %}
sudo apt-get install apache2
{% endhighlight %}

By default, the installed Apache instance is bound to port 80 and any host.

Make sure the instance not bound to a specific ip or host.

## enable mod_rewrite

When installing Apache, `mod_rewrite` might not be installed by default.

Under Ubuntu, just add a link in directory `/etc/apache2/mods-enabled` to the `rewrite.load` file in `/etc/apache2/mods-available`;

{% highlight sh %}
cd /etc/apache2/mods-enabled
ln -s ../mods-available/rewrite.load
{% endhighlight %}

# Modify the default host

## use a dedicated conf file 

Open file `000-default.conf` where the default host is configured.

{% highlight sh %}
sudo vi /etc/apache2/sites-available/000-default.conf
{% endhighlight %}

The default host is bound to any host on port 80:

{% highlight apacheconf %}
<VirtualHost *:80>
{% endhighlight %}

Add an `Include` directive before the closing tag of the `VirtualHost` directive to import the configuration file where you will write your Rewrite rules.
This is optional but you will find it convenient to clean your installation later or disable all changes you made by just commenting this directive.

{% highlight apacheconf %}
Include /etc/apache2/sites-available/my_rewrite_rule_tests.conf
{% endhighlight %}

## mod_rewrite logging

### enable logging

Inside the `VirtualHost` directive, look for the [`LogLevel` directive](http://httpd.apache.org/docs/2.4/en/mod/mod_rewrite.html#logging), it may be commented out, or add it.

What matters is having an argument to the directive starting with `rewrite`, such as the following:

{% highlight sh %}
LogLevel alert rewrite:trace8
{% endhighlight %}

The part after the colon in `rewrite:trace8` is the logging level.

As we are testing locally, we can use the maximum logging level (level8) but be aware that it should be used carefull (don't go lower than trace3) as mod_rewrite quickly gets extremely verbose.

### read mod_rewrite logs

mod_rewrite logs into `/var/log/apache2/error.log` with a `[rewrite` prefix.

{% highlight sh %}
tail -f /var/log/apache2/error.log | fgrep '[rewrite:' 
{% endhighlight %}

# Add hosts to /etc/hosts

The point here is to make any hostname involved in our rewrite rules point to the local computer (127.0.O.1).

You can then test rewrite rule based on existing host but also on non existing ones.

>for existing host, make sure you revert modifications in `/etc/hosts` after your are done testing. Otherwise, if you added `wwww.google.com` and bound it to `localhost` in `/etc/hosts` you won't be able to reach the real Google website

Open `/etc/hosts` (sudo required):

{% highlight sh %}
sudo vi /etc/hosts
{% endhighlight %}

and add a line such as the following:

{% highlight sh %}
127.0.0.1    store.mydomain.com boutique.mydomain.com
{% endhighlight %}

### bind Apache to hostnames

Add a `ServerName` directive (if none is already set yet) and any number of `ServerAlias` directive to bind Apache to hostnames you defined in `/etc/hosts`.

My advice is to add these directive to the dedicated configuration file created earlier.

{% highlight apacheconf %}
ServerName              store.mydomain.com
ServerAlias             boutique.mydomain.com
{% endhighlight %}

### add rewrite rules

Make sure the mod_rewrite engine is enabled by adding the `RewriteEngine` directive:

{% highlight apacheconf %}
RewriteEngine   On
{% endhighlight %}

Now, add your [RewriteRule](http://httpd.apache.org/docs/2.4/en/mod/mod_rewrite.html#rewriterule), [RewriteCond](http://httpd.apache.org/docs/2.4/en/mod/mod_rewrite.html#rewritecond) and [RewriteMap](http://httpd.apache.org/docs/current/en/mod/mod_rewrite.html#rewritemap) directives.

## test changes

You can either start/restart or reload Apache after each change.

{% highlight sh %}
sudo /etc/init.d/apache2 start
sudo /etc/init.d/apache2 restart
# only reload the configuration without restarting Apache
sudo /etc/init.d/apache2 reload
{% endhighlight %}

Now, open your favorite browser, type in a URL to test, see the result in the browser: are you being redirected or not? to the correct URL?

It does really matter if the URL your are being redirect to actually exists, worse case scenario, you'll get a 404 error but you will know if the rewrite rule worked.

If it is not working, check out the logs.

At log level `trace8` every operations run by mod_rewrite is visible. This even convenient to understand how the mod and directives work.
