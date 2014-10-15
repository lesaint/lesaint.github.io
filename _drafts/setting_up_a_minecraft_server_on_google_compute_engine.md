
#### create instance

```sh
gcloud compute instances create minecraft-server --image debian-7 --zone europe-west1-a
```

# TODO: use existing disk
# 
# TODO: specify machine type (gcloud compute machine-types list --zone europe-west1-a)
# --machine-type g1-small
# TODO: disable disk autodelete with 
# --disk auto-delete=no
# TODO: add tag MINECRAFT to match firewall rule
# --tags MINECRAFT

#### describe instance

gcloud compute instances describe minecraft-server --zone europe-west1-a

#### add firewall rule to allow minecraft connections

gcloud compute firewall-rules create allow-minecraft --description "Incoming minecraft connections allowed." --allow tcp:25565

# TODO : define target tag to restrict the firewall rule to only minecraft servers
# --target-tags MINECRAFT

#### connect to instance

gcloud compute ssh minecraft-server --zone europe-west1-a


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
echo "cd /home/lesaint/minecraft && /home/lesaint/jdk/bin/java -jar /home/lesaint/minecraft/minecraft_server.1.8.jar nogui" >> /home/lesaint/minecraft.sh
chmod +x /home/lesaint/minecraft.sh

# TODO: tune java

#### configure Minecraft

echo "eula=TRUE" > /home/lesaint/minecraft/eula.txt

# TODO: use whitelist.json to restrict connections

#### start the server

/home/lesaint/minecraft.sh

# TODO: make the minecraft server start by itself and run in the background
