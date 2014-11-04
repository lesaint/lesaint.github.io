---
layout: post
title: "Testing host-based Apache RewriteRule locally"
tags:
 - Apache
 - Ubuntu
 - testing
categories:
 - tips
image:
 feature: feature_image_green.png
---

Recently, I had to write a bunch of RewriteRule for Apache which applied to the whole URL, including the hostname.
I initially though this would be difficult to test locally but, in fact, with a modification of the `/etc/hosts` file, it's pretty easy.


# testing any RewriteRule

I will detailed here how I set up my computer to test these host-based rewrite rules. But, this article applies to testing *any* rewrite rule.

Some online tools such as [htaccess tester](http://htaccess.madewithlove.be/) exists and can come in handy for simple rules but that are limited by design.
For example, they can not supporte RewriteMap.

> when working rules, [regex101.com](http://regex101.com/#pcre) is pretty usefull to test regular expressions. Be sure to be in "pcre" mode has this is the intepretor used by Apache.

This can be used to test RewriteRule without any limitation and with as much debug information as provided by Apache.

# local setup

## Install Apache2

Installation under Ubuntu is trivial:

```sh
sudo apt-get install apache2
```

By default, the installed Apache instance is bound to port 80 and any host.

Make sure the instance not bound to a specific ip or host.

## add hosts under test to `/etc/hosts`

Open `/etc/hosts`:

```sh
sudo vi /etc/hosts
```

and add a line such as the following:

```sh
127.0.0.1    store.mydomain.com boutique.mydomain.com
```

Note that what is written in `/etc/hosts` takes precedence over the DNS.

## modify the default host

Open file `000-default.conf` where the default host is configured.

```sh
sudo vi /etc/apache2/sites-available/000-default.conf
```

The default host is bound to any host on port 80:

```xml
<VirtualHost *:80>
```

Add an `Include` directive to add the file where you will write your Rewrite rules.
This is optional but you will find it convenient to clean your installation later or disable all changes you made by just commenting this directive.

```
Include /etc/apache2/sites-available/my_rewrite_rule_tests.conf
```

## enable mod_rewrite

When installing Apache, `mod_rewrite` might not be installed by default.

Under Ubuntu, just add a link in directory `/etc/apache2/mods-enabled` to the `rewrite.load` file in `/etc/apache2/mods-available`;

```sh
cd /etc/apache2/mods-enabled
ln -s ../mods-available/rewrite.load
```

## mod_rewrite logging

### enable logging

Go back to the `000-default.conf` file and modify the defaut host.

Look for the `LogLevel` directive, it may be commented out, or add it.

What matters is having an argument to the directive starting with `rewrite`, such as the following:

```
LogLevel alert rewrite:trace8
```

The part after the colon in `rewrite:trace8` is the logging level.
As we are testing locally, we can use the maximum logging level (level8) but be aware that it shouldn't be used in production as this logging level is extremely verbose for mod_rewrite.

### read mod_rewrite logs

mod_rewrite logs into `/var/log/apache2/error.log` with a `[rewrite` prefix.

```sh
tail -f /var/log/apache2/error.log | fgrep '[rewrite:' 
```

## adding rules to test

If you followed my advice above to create a specific config file, you should modify the `/etc/apache2/sites-available/my_rewrite_rule_tests.conf`, otherwise just modify the default host directly.

### make Apache listen to the hostnames

Add directive to set a `ServerName` (if none is already set yet) and any number of `ServerAlias` required by the RewriteRule you'll be working on.
These host names should match those you added to `/etc/hosts` to be of any use:

```
ServerName              store.mydomain.com
ServerAlias             boutique.mydomain.com
```

### add your rewrite rules

The only mandatory directorive is the following to enable mod_rewrite:

```
RewriteEngine   On
```

But, obviously, you will also add [RewriteRule](http://httpd.apache.org/docs/2.4/en/mod/mod_rewrite.html#rewriterule), [RewriteCond](http://httpd.apache.org/docs/2.4/en/mod/mod_rewrite.html#rewritecond) and [RewriteMap](http://httpd.apache.org/docs/current/en/mod/mod_rewrite.html#rewritemap) conditions.

## test changes

You can either start/restart or reload Apache after each change.

```
sudo /etc/init.d/apache2 start
sudo /etc/init.d/apache2 restart
# only reload the configuration without restarting Apache
sudo /etc/init.d/apache2 reload
```
