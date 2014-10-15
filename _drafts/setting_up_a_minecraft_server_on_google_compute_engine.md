
## create instance

### create new instance with new disk

```sh
gcloud compute instances create minecraft-server --image debian-7 --zone europe-west1-a
```

> creates an instance called 'minecraft-server', a new boot disk from a debian 7 image, which will be deleted when the instance is destroyed and uses default machine type (n1-standard-1)

### create new instance with existing disk

```sh
gcloud compute instances create minecraft-server --zone europe-west1-a --disk name=minecraft-server boot=yes auto-delete=no --tags MINECRAFT
```

# TODO: use existing disk
# --disk name=minecraft-server boot=yes auto-delete=no
# TODO: specify machine type (gcloud compute machine-types list --zone europe-west1-a)
# --machine-type g1-small
# TODO: disable disk autodelete with 
# --disk auto-delete=no
# TODO: add tag ```minecraft``` to match firewall rule (uppercase letters are not valid)
# --tags minecraft

#### describe instance

gcloud compute instances describe minecraft-server --zone europe-west1-a

#### add firewall rule to allow minecraft connections

gcloud compute firewall-rules create allow-minecraft --description "Incoming minecraft connections allowed." --allow tcp:25565

# TODO : define target tag to restrict the firewall rule to only minecraft servers
# --target-tags MINECRAFT

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

