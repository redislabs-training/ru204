# Admin Training VM Setup - Stage 1

Here are steps to build the VM image from Ubuntu 18.04 with:
- Docker networking
- vanilla VNC
- vanilla DNS
- Redis Insight

Nodes will run in containers, but they look like VMs as shown.

![](img/00-vm-overview.png)

All students need is the VM's public IP and VNC password (provided by instructor).

Setup is built in three stages:
1. Start Docker, VNC, DNS
2. Configure DNS
2. Configure VNC.

For easy re-config, each stage produces a snapshot, image, and template.

Stages 2 and 3 also produce re-usable Docker images for DNS and VNC config.

Docker images are stored in GCR.

## Create a VPC and VM

1. Create a VPC in GCP with subnet 172.18.0.0/16 in the region where you want to run VMs.

Requirement | Specification
------------|--------------
Name | ***training***
Subnet Creation Mode | Custom
Subnet Name | ***training-subnet***
Subnet IP Address Range | 172.18.0.0/16

2. Create a firewall rule that allows ingress on all ports from all sources (0.0.0.0/0) to all targets.
 
3. Create the base VM in the region and VPC where you want to run instances.
  
Requirement  | Specification  
------------ | -------------
Name | ***admin-training-1***
Zone | us-west1-b
CPU | 4
Memory | 15 GB
OS | Ubuntu 18.04 LTS
Disk | 30 GB
Networking | ***training***
  
## SSH to the VM

1. SSH to the base VM from GCP console to finish setup.

2. Install vim and add ***trainee*** user to the ***docker*** group so users can start, stop, and SSH to containers.

```bash 
sudo su
apt -y update
apt -y install vim
 
```

```bash
update-alternatives --config editor <<< 3

adduser --disabled-password --gecos "" trainee
groupadd docker
usermod -aG docker trainee
 
```

3. Install Docker.

```bash
apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common <<< Y
    
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

apt-key fingerprint 0EBFCD88
   
add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

apt-get update
apt-get -y install docker-ce
 
```

4. Run ***sudo visudo*** and add the following line so ***trainee*** can start and stop containers without ***sudo***.

```bash
trainee ALL=(ALL) NOPASSWD:ALL
```


5. Switch to ***trainee*** user to create the Docker network, add scripts, and build the initial VNC Docker image and run it as an unconfigured (vanilla) container.

```bash
sudo su - trainee
 
```

6. Uncomment the following line in the user's ***.bashrc*** file so the base VM prompt is ***green*** and you can tell it apart from the ***yellow*** VNC container prompt.

```bash
#force_color_prompt
```

7. Create the Docker network.

```bash
docker network create --subnet=172.18.0.0/16 rlabs
 
```

8. Run the Xfce VNC container so the VM has a UI.

```bash
docker run --name vanilla-vnc  -d -e VNC_PW=trainee! --restart=always --net rlabs --hostname vnc-terminal.rlabs.org --ip 172.18.0.2 -p 80:6901 consol/ubuntu-xfce-vnc
 
```

9. Run ***Redis Insight*** so students can view databases in a UI.

```bash
docker run --name insight -d -v redisinsight:/db --restart=always --net rlabs --dns 172.18.0.20 --hostname insight.rlabs.org --ip 172.18.0.4  redislabs/redisinsight
 
```

10. Run ***BIND*** DNS so node and cluster names can be resolved on your private network.

```bash
docker run --name vanilla-dns -d --restart=always --net rlabs --dns 172.18.0.20 --hostname ns.rlabs.org --ip 172.18.0.20 -p 10000:10000/tcp  sameersbn/bind
 
```

***SKIP:*** Someday, you may use ***CoreDNS*** with Corefile and rlabs.db.

```bash
docker run --name vanilla-dns -d -v /home/trainee/coredns/:/root/ --restart=always --net rlabs --dns 172.18.0.20 --hostname ns.rlabs.org --ip 172.18.0.20  coredns/coredns -conf /root/Corefile
```

## Test VNC and DNS access

1. Point your laptop browser to the VMs public IP (found in GCP console).

2. Sign in to VNC with password ***trainee!*** .

3. Open Chrome in VNC desktop.

4. Point it to https://172.18.0.20:10000 (this is ***BIND***'s admin console).

5. Sign in with ***root*** and ***password*** .

6. Close Chrome.

Now you have:
- Docker network
- vanilla VNC
- vanilla DNS
- Redis Insight.

### Save your work

1. Create a snapshot of the VM called ***admin-training-1***.

2. Create an image from the snapshot called ***admin-training-1***.

3. Create a template from the image called ***admin-training-1***.
