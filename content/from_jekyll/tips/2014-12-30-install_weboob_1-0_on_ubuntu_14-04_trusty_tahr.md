Title: Install Weboob 1.0 on Ubuntu 14.04 (Trusty Tahr)
Tags: weboob, Ubuntu

As stated on the Weboob [install page](http://weboob.org/install), Ubuntu packages for [Weboob](http://weboob.org/) are lagging behind (a lot). Package for the current LTS version of Ubuntu (14.04 - Trusty Tahr) is version 0.g-1 (can find how old this version is). The current version of Weboob (version 1.0, out October 2014) is packaged for Ubuntu 15.04 (Vivid Vervet).

So, here is how I installed from source the latest stable version of Weboob (1.0) on Ubuntu 14.04 (Trusty Tahr).


As stated on the website "Weboob is a collection of applications able to interact with websites, without requiring the user to open them in a browser. It also provides well-defined APIs to talk to websites lacking one". 

Perso:qnally, I use Weboob to access my bank website and retrieve my history and incoming operations data from the command line to process it.

# checkout Git source

create a Weboob directory:

```bash
sudo mkdir /opt/weboob
```

checkout Weboob stable sources :

```bash
$ mkdir /tmp/weboob
$ cd /tmp/weboob
$ git clone git://git.symlink.me/pub/weboob/stable.git src
```

# Install dependencies

## Python basics

Install Python 2.7

```bash
$ sudo apt-get install python2.7
```

Install setuptools

by hand (cf. [https://pypi.python.org/pypi/setuptools#unix-wget](https://pypi.python.org/pypi/setuptools#unix-wget)):

```bash
$ wget https://bootstrap.pypa.io/ez_setup.py -O - | sudo python
```

>note: I though for a minute that the `ez_setup.py` program was stuck but it turned out that the prompt for the sudo password was lost in the middle of noisy logs. So, if it happends to you, just it `enter`, you will be prompted for the sudo password again.

or with apt-get (not sure the version of setuptools is recent enough, though, I used the manual instal):

```bash
sudo apt-get install python-setuptools
```

## Dependencies for Weboob

Install dependencies for Weboob:

```bash
$ sudo apt-get install python-requests
```

## Dependencies for boobank

Currently, the only module I use is boobank, which has dependencies of its own:

```bash
$ sudo apt-get install python-dateutil python-prettytable python-mechanize python-cssselect
```

# Local install

We will do a local install of Weboob as the system install is discouraged on the [Weboob instal page](http://weboob.org/install).

Create `bin` directory in your home directory (if it does not exist yet). This is where we will be telling the local installation tool to create the Weboob executable:

```bash
$ mkdir ~/bin
```

and run the local installer:

```bash
$ cd /tmp/weboob/src
$ ./tools/local_install.sh ~/bin
```

# verify install

Add the `~/bin` directory to your PATH (if it not already), you can then just type `boobank`.

In the meantime, you can make sure the install directly by running:

```bash
$ ~/bin/boobank
```



