# Admin Training VM Setup - Stage 1

Here are steps to build ***admin-training-1*** from Ubuntu 18.04.

You'll end up with:
- Docker networking
- Vanilla DNS
- Vanilla VNC
- Redis Insight
- Node containers - stopped and removed.

Nodes run in containers, but they look like VMs.

![](img/00-vm-overview.png)

All students need is the VM's public IP and VNC password (provided by instructor).

Setup is built in three stages:
1. Start Docker, DNS, VNC, nodes
2. Configure DNS
2. Configure VNC.

For easy re-config, each stage produces a VM snapshot, image, and template.

Stages 2 and 3 also produce Docker images for DNS and VNC.

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
Labels | creator, version, os
CPU | 4
Memory | 15 GB
OS | Ubuntu 18.04 LTS
Disk | 30 GB
Delete protection | enabled
Networking | ***training***
  
## Install Docker

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

4. Run 

```bash
sudo visudo
 
```

and add the following line so ***trainee*** can start and stop containers without ***sudo***.

```bash
trainee ALL=(ALL) NOPASSWD:ALL
```


5. Switch to ***trainee*** user to create the Docker network, add scripts, and build the initial VNC Docker image and run it as an unconfigured (vanilla) container.

```bash
sudo su - trainee
 
```

6. Run

```bash
vi .bashrc
 
```
and uncomment the following line so ***trainee***'s base VM prompt is ***green*** and you can tell it apart from the ***yellow*** VNC user prompt.

```bash
#force_color_prompt
```

7. Create the Docker network.

```bash
docker network create --subnet=172.18.0.0/16 rlabs
 
```

8. Run ***BIND*** DNS so URLs can get resolved on the Docker network (config is done in stage 2).

```bash
docker run --name vanilla-dns -d --restart=always --net rlabs --dns 172.18.0.20 --hostname ns.rlabs.org --ip 172.18.0.20 -p 10000:10000/tcp  sameersbn/bind
 
```

***SKIP:*** Someday, you may use ***CoreDNS*** with Corefile and rlabs.db.

```bash
docker run --name vanilla-dns -d -v /home/trainee/coredns/:/root/ --restart=always --net rlabs --dns 172.18.0.20 --hostname ns.rlabs.org --ip 172.18.0.20  coredns/coredns -conf /root/Corefile
```

9. Run ***Xfce VNC*** so the VM has a UI on port 80 (config is done in stage 3).

```bash
docker run --name vanilla-vnc  -d -e VNC_PW=trainee! --restart=always --net rlabs --hostname vnc-terminal.rlabs.org --ip 172.18.0.2 -p 80:6901 consol/ubuntu-xfce-vnc
 
```

10. Run ***Redis Insight*** so students can explore databases in a UI.

```bash
docker run --name insight -d -v redisinsight:/db --restart=always --net rlabs --dns 172.18.0.20 --hostname insight.rlabs.org --ip 172.18.0.4  redislabs/redisinsight
 
```

## Add scripts to run nodes and create clusters

1. Scripts run on the base VM, but are run by students from the VNC container via alias commands

```bash
mkdir scripts

cat << EOF > scripts/start_north_nodes.sh
RED='\e[31;1m'
GREEN='\e[32;1m'
YELLOW='\e[33;1m'
BLUE='\e[34;1m'
MAGENTA='\e[35;1m'
CYAN='\e[36;1m'
RED2='\e[31m'
GREEN2='\e[32m'
YELLOW2='\e[33m'
BLUE2='\e[34m'
MAGENTA2='\e[35m'
CYAN2='\e[36m'
NC='\e[0m'

# had to add '\' before every color variable '\${GREEN}'
# otherwise copy-paste to 'cat' dereferences each variable during copy-paste when building initial VM image

sleep 1 
printf "Removing old nodes... "
docker kill n1  >/dev/null 2>&1; docker rm n1  >/dev/null 2>&1
docker kill n2  >/dev/null 2>&1; docker rm n2  >/dev/null 2>&1
docker kill n3  >/dev/null 2>&1; docker rm n3  >/dev/null 2>&1
echo -e "\${GREEN}ok\${NC}"

sleep 1
printf "Starting new nodes... "
docker run --name n1 -d --restart=always --cap-add=ALL --net rlabs --dns 172.18.0.20 --hostname n1.rlabs.org --ip 172.18.0.21 redislabs/redis >/dev/null
docker run --name n2 -d --restart=always --cap-add=ALL --net rlabs --dns 172.18.0.20 --hostname n2.rlabs.org --ip 172.18.0.22 redislabs/redis  >/dev/null
docker run --name n3 -d --restart=always --cap-add=ALL --net rlabs --dns 172.18.0.20 --hostname n3.rlabs.org --ip 172.18.0.23 redislabs/redis  >/dev/null
echo -e "\${GREEN}ok\${NC}"

sleep 1
printf "Changing prompt colors... "
docker exec n1 bash -c "echo \"export PS1='\u@\${MAGENTA}[Node-N1]\${NC}:\${MAGENTA2}\w\${NC}$ '\" >> ~/.bashrc"
docker exec n2 bash -c "echo \"export PS1='\u@\${YELLOW}[Node-N2]\${NC}:\${YELLOW2}\w\${NC}$ '\" >> ~/.bashrc"
docker exec n3 bash -c "echo \"export PS1='\u@\${GREEN}[Node-N3]\${NC}:\${GREEN2}\w\${NC}$ '\" >> ~/.bashrc"
echo -e "\${GREEN}ok\${NC}"

sleep 1
printf "Creating IP routes - wait 60 seconds... "
docker exec --user root n1 bash -c "iptables -t nat -I PREROUTING -p udp --dport 53 -j REDIRECT --to-ports 5300  >/dev/null"
docker exec --user root n2 bash -c "iptables -t nat -I PREROUTING -p udp --dport 53 -j REDIRECT --to-ports 5300  >/dev/null"
docker exec --user root n3 bash -c "iptables -t nat -I PREROUTING -p udp --dport 53 -j REDIRECT --to-ports 5300  >/dev/null"
sleep 60
echo -e "\${GREEN}ok\${NC}"

sleep 1
echo -e "\${GREEN}Done\${NC} - Closing connection... "
sleep 2
EOF

cat << EOF > scripts/start_south_nodes.sh
RED='\e[31;1m'
GREEN='\e[32;1m'
YELLOW='\e[33;1m'
BLUE='\e[34;1m'
MAGENTA='\e[35;1m'
CYAN='\e[36;1m'
RED2='\e[31m'
GREEN2='\e[32m'
YELLOW2='\e[33m'
BLUE2='\e[34m'
MAGENTA2='\e[35m'
CYAN2='\e[36m'
NC='\e[0m'

sleep 1
printf "Removing old nodes... "
docker kill s1  >/dev/null 2>&1; docker rm s1  >/dev/null 2>&1
docker kill s2  >/dev/null 2>&1; docker rm s2  >/dev/null 2>&1
docker kill s3  >/dev/null 2>&1; docker rm s3  >/dev/null 2>&1
echo -e "\${GREEN}ok\${NC}"

sleep 1
printf "Starting new nodes... "
docker run --name s1 -d --restart=always --cap-add=ALL --net rlabs --dns 172.18.0.20 --hostname s1.rlabs.org --ip 172.18.0.31 redislabs/redis  >/dev/null
docker run --name s2 -d --restart=always --cap-add=ALL --net rlabs --dns 172.18.0.20 --hostname s2.rlabs.org --ip 172.18.0.32 redislabs/redis  >/dev/null
docker run --name s3 -d --restart=always --cap-add=ALL --net rlabs --dns 172.18.0.20 --hostname s3.rlabs.org --ip 172.18.0.33 redislabs/redis  >/dev/null
echo -e "\${GREEN}ok\${NC}"

sleep 1
printf "Changing prompt colors... "
docker exec s1 bash -c "echo \"export PS1='\u@\${MAGENTA}[Node-S1]\${NC}:\${MAGENTA2}\w\${NC}$ '\" >> ~/.bashrc"
docker exec s2 bash -c "echo \"export PS1='\u@\${YELLOW}[Node-S2]\${NC}:\${YELLOW2}\w\${NC}$ '\" >> ~/.bashrc"
docker exec s3 bash -c "echo \"export PS1='\u@\${GREEN}[Node-S3]\${NC}:\${GREEN2}\w\${NC}$ '\" >> ~/.bashrc"
echo -e "\${GREEN}ok\${NC}"

sleep 1
printf "Creating IP routes - wait 60 seconds... "
docker exec --user root s1 bash -c "iptables -t nat -I PREROUTING -p udp --dport 53 -j REDIRECT --to-ports 5300  >/dev/null"
docker exec --user root s2 bash -c "iptables -t nat -I PREROUTING -p udp --dport 53 -j REDIRECT --to-ports 5300  >/dev/null"
docker exec --user root s3 bash -c "iptables -t nat -I PREROUTING -p udp --dport 53 -j REDIRECT --to-ports 5300  >/dev/null"
sleep 60
echo -e "\${GREEN}ok\${NC}"

sleep 1
echo -e "\${GREEN}Done\${NC} - Closing connection... "
sleep 2
EOF

cat << EOF > scripts/create_north_cluster.sh
GREEN='\e[32;1m'
NC='\e[0m'
docker exec -it n1 bash -c "/opt/redislabs/bin/rladmin cluster create persistent_path \
        /var/opt/redislabs/persist ephemeral_path /var/opt/redislabs/tmp addr 172.18.0.21 \
        name north.rlabs.org username admin@rlabs.org password admin";
docker exec -it n2 bash -c "/opt/redislabs/bin/rladmin cluster join persistent_path \
        /var/opt/redislabs/persist ephemeral_path /var/opt/redislabs/tmp addr 172.18.0.22 \
        username admin@rlabs.org password admin nodes 172.18.0.21";
docker exec -it n3 bash -c "/opt/redislabs/bin/rladmin cluster join persistent_path \
        /var/opt/redislabs/persist ephemeral_path /var/opt/redislabs/tmp addr 172.18.0.23 \
        username admin@rlabs.org password admin nodes 172.18.0.21";
sleep 1
echo -e "\${GREEN}Done\${NC} - Closing connection... "
sleep 2
EOF

cat << EOF > scripts/create_south_cluster.sh
GREEN='\e[32;1m'
NC='\e[0m'
docker exec -it s1 bash -c "/opt/redislabs/bin/rladmin cluster create persistent_path \
        /var/opt/redislabs/persist ephemeral_path /var/opt/redislabs/tmp addr 172.18.0.31 \
        name south.rlabs.org username admin@rlabs.org password admin";
docker exec -it s2 bash -c "/opt/redislabs/bin/rladmin cluster join persistent_path \
        /var/opt/redislabs/persist ephemeral_path /var/opt/redislabs/tmp addr 172.18.0.32 \
        username admin@rlabs.org password admin nodes 172.18.0.31";
docker exec -it s3 bash -c "/opt/redislabs/bin/rladmin cluster join persistent_path \
        /var/opt/redislabs/persist ephemeral_path /var/opt/redislabs/tmp addr 172.18.0.33 \
        username admin@rlabs.org password admin nodes 172.18.0.31";
sleep 1
echo -e "\${GREEN}Done\${NC} - Closing connection... "
sleep 2
EOF

cat << EOF > scripts/run_dnsutils.sh
docker kill dnsutils  >/dev/null 2>&1; docker rm dnsutils  >/dev/null 2>&1
docker run --name dnsutils -it --net rlabs --dns 172.18.0.20 --hostname dnsutils.rlabs.org --ip 172.18.0.6 tutum/dnsutils 
EOF

# make the scripts executable
chmod 755 scripts/start_north_nodes.sh
chmod 755 scripts/start_south_nodes.sh
chmod 755 scripts/create_north_cluster.sh
chmod 755 scripts/create_south_cluster.sh
chmod 755 scripts/run_dnsutils.sh
 
```

## Check VNC and DNS access

1. Point your laptop browser to the VMs public IP (found in GCP console).

2. Sign in to VNC with password ***trainee!*** .

3. Open Chrome in VNC desktop.

4. Point it to https://172.18.0.20:10000 (this is ***BIND***'s admin console).

5. Sign in with ***root*** and ***password*** .

## Check node and cluster creation

1. From the GCP shell terminal, start nodes:

```bash
scripts/start_north_nodes.sh
 
```

2. Create the ***north*** cluster

```bash
scripts/create_north_cluster.sh
 
```

3. From VNC desktop, point Chrome at https://n1:8443

4. Sign in with ***admin@rlabs.org*** and ***admin*** .

5. Click ***nodes*** to make sure the cluster was created.

6. In GCP shell terminal, stop and remove nodes.

This forces manual restart so clusters build and resolve DNS properly. 

```bash
docker stop n1 n2 n3
docker rm n1 n2 n3
 
```

Now you have:
- Docker networking
- Vanilla DNS
- Vanilla VNC
- Redis Insight
- Node containers - stopped and removed.

## Save your work

1. Create a snapshot of the VM called ***admin-training-1***.

2. Create an image from the snapshot called ***admin-training-1***.

3. Create an instance template from the image called ***admin-training-1***.
