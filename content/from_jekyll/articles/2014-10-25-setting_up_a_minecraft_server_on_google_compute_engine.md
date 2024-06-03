Title: Setting up a Minecraft server on Google Compute Engine
Tags: Cloud, Minecraft, Google Compute Engine

This article will get you through the (few) steps to set up a Minecraft server on a Google Compute Engine instance.


[TOC]

# Create Google Cloud account

Go to [https://console.developers.google.com/project](https://console.developers.google.com/project).

This is the Google Developer Console and entry point to the Google Cloud services. You need to login with a Google account.

If you already have Gmail and you are connected, the page will display without any authentication.

## create project

In the Google Developer Console, go to ```projects``` and create a new one.

The name of the project is for your own convenience. Google will generate a human readable project id which is the value you will need to identify a project when using the [Google Cloud SDK](#install-google-cloud-sdk).

## provide billing info

Billing info are required to use Google Compute Engine because creating an instance or a disk will cost you from the first minute (but, so little...).

# Google Cloud SDK

## install it

My installation setup is described in [Installing Google Cloud SDK on Ubuntu with Oh-My-Zsh]({filename/from_jekyll/tips/2014-10-17-installing_google_cloud_sdk_on_ubuntu_with_oh-my-zsh.md).

## authenticate

Run:

```sh
gcloud auth init
```

Go to your browser, authenticate or choose a Google account if necessary and authorize the Google Cloud SDK on your computer to access your Google Account.

## set project

You can either set a project globally with the following command:

```sh
gcloud config set project cagoo-jimba-2345
```

or create a directory for your project so that you can then switch from one project to the other by just changing the current directory:

```sh
cd /some/dir/where/you/can/to/create/googlecloud/project/directories
gcloud init cagoo-jimba-2345
```

# create an instance

## create a disk

The point here is to set up an instance with a Minecraft server but as we will see below, the instance itself can be created and destroyed at will.

What matters really is the disk where Minecraft server program is set up and where the world's data is stored. As long as we keep the disk, we can create a new instance latter with the same disk and it will feel as it was still the first instance.

So, we start by creating a disk:

```sh
gcloud compute disks create minecraft-server --image debian-7 --zone europe-west1-a
```

>this will create a standard disk (non-SSD) of 10Gb from a debian 7 image

## create an instance with an existing disk

```sh
gcloud compute instances create minecraft-server --zone europe-west1-a --disk name=minecraft-server boot=yes auto-delete=no --tags minecraft
```

* use existing disk and keep it even when VM is deleted
```sh
    --disk name=minecraft-server boot=yes auto-delete=no
```
* add tag ```minecraft``` to match firewall rule (uppercase letters are not valid)
```sh
    --tags minecraft
```

# allow Minecraft traffic

```sh
gcloud compute firewall-rules create allow-minecraft --description "Incoming minecraft connections allowed." --allow tcp:25565 --target-tags minecraft
```

>allow tcp traffic on port `25565`, which is the default port used by Minecraft server. You can make sure your Minecraft server is listening to this port by checking the first log lines of the server when it starts up.

* define target tag to restrict the firewall rule to only instances with the tag `minecraft`
```sh
    --target-tags minecraft
```

# connect to the instance with SSH

```sh
gcloud compute ssh minecraft-server --zone europe-west1-a
```

If this is the first time you attempt to connect to an instance via SSH with the current Google Cloud SDK installation, you will be asked to create a private-public key paar. Just follow the instructions. Note that it is best to define a passphrase to protect your keys.

# install the instance

## required basics

You will need `vim` to edit files and `screen` to run the Minecraft server without being connected to the instance.

```sh
sudo apt-get update
sudo apt-get install vim screen
```

## download and install Oracle Java

```sh
# downlad and unpack Java JDK 8 8u5-b13
wget --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" -qO- http://download.oracle.com/otn-pub/java/jdk/8u5-b13/jdk-8u5-linux-x64.tar.gz | tar xvz
# create symbolic link to allow update of Java without changing the rest
ln -s jdk1.8.0_05 jdk
```

>Found out how to download the JDK from Oracle website thanks to this StackOverflow post [How to automate download and installation of Java JDK on Linux?](http://stackoverflow.com/questions/10268583/how-to-automate-download-and-installation-of-java-jdk-on-linux).

### note on open-jdk

Alternatively you could install `open-jdk` via `apt-get` but I found it requires installing to much stuff on the server (and takes much more time) so I rather went with installing Oracle JDK.

FYI, the command line is:

```sh
sudo apt-get install -y openjdk-8-jre
```

## download and install Minecraft

```sh
mkdir minecraft
cd minecraft
wget https://s3.amazonaws.com/Minecraft.Download/versions/1.8/minecraft_server.1.8.jar

echo '#!/bin/bash
cd /home/lesaint/minecraft && /home/lesaint/jdk/bin/java -jar /home/lesaint/minecraft/minecraft_server.1.8.jar -Xmx1024M -Xms1024M nogui' > /home/lesaint/minecraft.sh
chmod +x /home/lesaint/minecraft.sh
```

>this script starts the Minecraft server with 1Gb heap. Make sure you choose an instance with enough memory or change the `-Xmx` and `-Xms` values.

Minimal configuration needed is to create a file which Minecraft will read to know whether you accepted the Minecraft EULA or not.

When run for the first time, Minecraft server create the file and asks you to modify it and restart the server.

To save one server run, we just create it ourselves.

```sh
echo "eula=TRUE" > /home/lesaint/minecraft/eula.txt
```

# start the server

```sh
/home/lesaint/minecraft.sh
```

You must stay connected to the instance for the Minecraft server to run, we will discuss below how to [let it run in the background](#let-it-run-in-the-background).

# connect to the server

The Minecraft server is running and you can now to connect to it with a Minecraft client (ie. the game).

## get the server's IP address

Use the following command to get the list of instances and, among other informations, you can find the external IP address of the one you just started:

```sh
gcloud compute instances list
```

Result will look like the following and we are interested in what is below `EXTERNAL_IP`:

```sh
[my-machine] $ gcloud compute instances list                                           
NAME             ZONE           MACHINE_TYPE  INTERNAL_IP   EXTERNAL_IP  STATUS
minecraft-server europe-west1-a n1-standard-1 10.240.197.56 104.155.10.4 RUNNING
```

## connect to the server

Start Minecraft, go to `Multiplayer`.

Either click `Direct connect` or `Add server`.

Specifity the server name if you clicked on `Add server` and specify the `EXTERNAL_IP` from above as `Server address`.

Now, connect and play :)

# let it run in the background

The problem when starting the Minecraft server from an SSH session is that the server's process will be ended when the SSH session is ended (ie. when you disconnect).

## use `screen`

To work around this, start the Minecraft server using [screen](http://www.gnu.org/software/screen/manual/screen.html). Screen has been installed when doing the [basic configuration of instance](#basic-configuration-of-instance) earlier.

### start the server

Start the Minecraft server in a new `screen` terminal window.

```sh
screen /home/lesaint/minecraft.sh
```

To exit `screen` without killing it, use ```CTRL+a d``` (type `CTRL+A` on your keyboard and then letter `d`). It is called "detaching" from the `screen` session.

You can check the Minecraft server java process is actually running with the following command line:

```sh
ps -ef | grep java
```

### get your hands back on the server

To "reattach" to the `screen` terminal, you must find its id. List all `screen` session on the current host with:

```sh
screen -list
```

Result will look like the following:

```sh
lesaint@minecraft-server:~$ screen -list
There is a screen on:
    2046.pts-1.minecraft-server (10/16/14 21:17:03) (Detached)
1 Socket in /var/run/screen/S-lesaint.
```

You can reattach to the `screen` session with the number at the beginning of the line:

```sh
screen -r 2046
```

From that point, you can manage the Minecraft server as you would be doing if you had started it from the SSH session directly.

### stop the server

To stop the server, reattach to the `screen` session and just type `CTRL+C`. It will stop the Minecraft server and if you started the `screen` session with the Minecraft service as an argument,it will also end the `screen` session. 

# destroy the instance

When you don't need the instance, destroy it as it will cost you even if it is not doing anything. Since it is so easy and quick to recreate it, do not hesitate.

What matters is the disk and it will not be deleted if you correctly specified ```auto-delete=no``` when creating the instance (see [create instance with existing disk](#create-an-instance-with-an-existing-disk)).

In doubt, go to the Google developer console, display the instance properties. A checkbox indicates whether the disk will be deleted when the instance is deleted. You can change the value directly from there.

```sh
gcloud compute instances delete minecraft-server --zone europe-west1-a
```
