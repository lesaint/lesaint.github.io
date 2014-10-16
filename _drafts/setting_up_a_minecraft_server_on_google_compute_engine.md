---
layout: post
title: "Setting up a Minecraft server on Google Compute Engine"
tags:
 - Minecraft
 - Google Compute Engine
categories:
 - articles
image:
 feature: feature_image_green.png
---

## Create Google Cloud account

Go to [https://console.developers.google.com/project](https://console.developers.google.com/project).

This is the Google Developer Console and entry point to the Google Cloud services. You need to login with a Google account.

If you already have Gmail and you are connected, the page will display without any authentication.

### create project

In the Google Developer Console, go to ```projects``` and create a new one.

The name of the project is for your own convenience. Google will generate a human readable project id which is the value you will need to identify a project when using the [Google Cloud SDK](#install-google-cloud-sdk).

### provide billing info

Billing info are required to use Google Compute Engine as creating an instance or a disk will cost you from the first minute (but, so little...).

## install Google Cloud SDK

My installation setup is described in [Installing Google Cloud SDK on Ubuntu with Oh-My-Zsh](TODO link to tip).

## authenticate with Google Cloud SDK

Run:

```sh
gcloud auth init
```

Go to your browser, authenticate or choose a Google account is necessary and authorise the Google Cloud SDK on your computer to access your Google Account.

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

## create instance

### create a disk

The point here is to set up a instance with a minecraft server but as we will see below, the instance itself can be created and destroyed at will.

What matters really is the disk where minecraft server program is set up and where the world's data is stored. As long as we keep the disk, we can create a new instance latter with the same disk and it will feel as it was still the first instance.

So, we start by creating a disk:

```sh
gcloud compute disks create minecraft-server --image debian-7 --zone europe-west1-a
```

>this will create a standard disk (non-SSD) of 10Gb from a debian 7 image

### create instance with existing disk

```sh
gcloud compute instances create minecraft-server --zone europe-west1-a --disk name=minecraft-server boot=yes auto-delete=no --tags minecraft
```

* use existing disk and keep it even when VM is deleted
    ```
    --disk name=minecraft-server boot=yes auto-delete=no
    ```
* add tag ```minecraft``` to match firewall rule (uppercase letters are not valid)
    ```
    --tags minecraft
    ```

#### allow minecraft traffic

```sh
gcloud compute firewall-rules create allow-minecraft --description "Incoming minecraft connections allowed." --allow tcp:25565 --target-tags MINECRAFT
```

* define target tag to restrict the firewall rule to only minecraft servers
    ```
    --target-tags MINECRAFT
    ```

#### connect to instance

```sh
gcloud compute ssh minecraft-server --zone europe-west1-a
```

#### basic configuration of instance

You will need `vim` to edit files and `screen` to run the minecraft server without beeing connected to the instance.

```sh
sudo apt-get update
sudo apt-get install vim screen
```

#### download Java and install

```sh
wget --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u5-b13/jdk-8u5-linux-x64.tar.gz
tar xvzf jdk-8u5-linux-x64.tar.gz
rm jdk-8u5-linux-x64.tar.gz
ln -s jdk1.8.0_05 jdk
```

#### download and install minecraft

```sh
mkdir minecraft
cd minecraft
wget https://s3.amazonaws.com/Minecraft.Download/versions/1.8/minecraft_server.1.8.jar

echo "#!/bin/bash" > /home/lesaint/minecraft.sh
echo "cd /home/lesaint/minecraft && /home/lesaint/jdk/bin/java -jar /home/lesaint/minecraft/minecraft_server.1.8.jar -Xmx1024M -Xms1024M nogui" >> /home/lesaint/minecraft.sh
chmod +x /home/lesaint/minecraft.sh
```

>this script starts the Minecraft server with 1Gb heap. Make sure you choose an instance with enough memory or change the `-Xmx` and `-Xms` values.

#### configure Minecraft

Minimal configuration needed is to create a file which minecraft will read to know wheter you accepted the Minecraft EULA or not.

When run for the first time, minecraft server create the file and asks you to modify it and restart the server.

To save one server run, we just create it ourselves.

```sh
echo "eula=TRUE" > /home/lesaint/minecraft/eula.txt
```

#### start the server

```sh
/home/lesaint/minecraft.sh
```

You must stay connected to the instance for the minecraft server to run, we will discuss below how to [let it run in the background](#let-it-run-in-the-background).

## connect to the server

The minecraft server is running and you can now to connect to it with a minecraft client (ie. the game).

### get the server's IP address

Use the following command to get the list of instance and, among other informations, it's external IP addresse:

```sh
gcloud compute instances list
```

Result will look like the following and we are interrested in what is below `EXTERNAL_IP`:

```sh
[my-machine] $ gcloud compute instances list                                           
NAME             ZONE           MACHINE_TYPE  INTERNAL_IP   EXTERNAL_IP  STATUS
minecraft-server europe-west1-a n1-standard-1 10.240.197.56 104.155.10.4 RUNNING
```

### connect to the server

Start minecraft, go to `Multiplayer`.

Either click `Direct connect` or `Add server`.

Specifity the server name if you clicked on `Add server` and specify the `EXTERNAL_IP` from above as `Server address`.

Play :)

### let it run in the background

The probleme when starting the minecraft server from an SSH session is that the server's process will be ended when the SSH session is ended (ie. when you disconnect).

To work around this, start the minecraft server using [screen](http://www.gnu.org/software/screen/manual/screen.html). Screen has been installed when doing the [basic configuration of instance](#basic-configuration-of-instance) earlier.

#### start the server

Start the minecraft server in a new `screen` terminal window.

```sh
screen /home/lesaint/minecraft.sh
```

To exit ```screen``` without killing it, use ```CTRL+a d``` (type `CTRL+A` on your keyboard and then letter `d`). It is called "detaching" from the screen session.

You can check the minecraft server java is actually running with the following command line:

```sh
ps -ef | grep java
```

#### get your hands back on the server

To "reattach" to the `screen` terminal, you must find its id. List all screen session on the current host with:

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

You can reattach to the screen session with the number at the beginning of the line:

```sh
screen -r 2046
```

From that point, you can manage the minecraft server as you would be doing if you had started it from the SSH session directly.

#### stop the server

To stop the server, reattach to the `screen` session and just type `CTRL+C`. If you started the `screen` session with the minecraft service as an argument, killing the minecraft server will also end the `screen` session. 

## destroy the instance

When you don't need the instance, destroy it as it will cost you even if it is not doing anything. Since it is so easy and quick to recreate it, do not hesitate. What matters is the disk and it will not be deleted.

```sh
gcloud compute instances delete minecraft-server --zone europe-west1-a
```

This should not delete the disk `minecraft-server` unless you have forgotten to disable the disk's autodelete when creating the instance (see [create instance with existing disk](#create-instance-with-existing-disk)).
