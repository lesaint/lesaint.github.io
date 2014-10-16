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

## create instance

### create new instance with new disk

```sh
gcloud compute instances create minecraft-server --image debian-7 --zone europe-west1-a
```

> creates an instance called 'minecraft-server', a new boot disk from a debian 7 image (which will be deleted when the instance is destroyed) and uses default machine type (n1-standard-1)

### create instance with existing disk

```sh
gcloud compute instances create minecraft-server --zone europe-west1-a --disk name=minecraft-server boot=yes auto-delete=no --tags MINECRAFT
```

* use existing disk and keep it even when VM is deleted
    ```
    --disk name=minecraft-server boot=yes auto-delete=no
    ```
* specify machine type (gcloud compute machine-types list --zone europe-west1-a)
    ```
    --machine-type g1-small
    ```
* add tag ```minecraft``` to match firewall rule (uppercase letters are not valid)
    ```
    --tags minecraft
    ```

### describe instance

```sh
gcloud compute instances describe minecraft-server --zone europe-west1-a
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

sudo apt-get update
sudo apt-get install vim

#### download Java and install

wget --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u5-b13/jdk-8u5-linux-x64.tar.gz
tar xvzf jdk-8u5-linux-x64.tar.gz
rm jdk-8u5-linux-x64.tar.gz
ln -s jdk1.8.0_05 jdk

#### download and install minecraft

mkdir minecraft
cd minecraft
wget https://s3.amazonaws.com/Minecraft.Download/versions/1.8/minecraft_server.1.8.jar

echo "#!/bin/bash" > /home/lesaint/minecraft.sh
echo "cd /home/lesaint/minecraft && /home/lesaint/jdk/bin/java -jar /home/lesaint/minecraft/minecraft_server.1.8.jar -Xmx1024M -Xms1024M nogui" >> /home/lesaint/minecraft.sh
chmod +x /home/lesaint/minecraft.sh

# TODO: tune java

#### configure Minecraft

echo "eula=TRUE" > /home/lesaint/minecraft/eula.txt

# TODO: use whitelist.json to restrict connections

#### start the server

/home/lesaint/minecraft.sh

# TODO: make the minecraft server start by itself and run in the background

## minecraft in Docker

TODO:
* run as daemon
* world must be stored out of the Docker process
    - can world directory be a symbolic link ?
    - can world directory configured to be somewhere else ?

