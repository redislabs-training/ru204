# VM Config - Stage 1

Here are steps to configure ***admin-training-1*** from instance template ***admin-training-0***.

Template includes:

Property | Value
---|---
Machine type | ***n1-standard-4***
Image | ***Ubuntu 18.04 LTS***
Disk size (GB) | ***30***
Network | ***training***
Subnet | ***training-subnet***
Region | ***us-west1***

This stage produces:
- Docker
- VNC
- Redis Insight
- RE Nodes.

## Create VM

1. Create the VM from ***admin-training-0***.

```bash
gcloud compute instances create admin-training-1 --source-instance-template admin-training-0 --zone=us-west1-b
 
```

## Add VI, user, and Docker 

1. SSH to the VM from GCP console.

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

## Create Docker network and run containers

1. Switch to ***trainee*** user. 

```bash
sudo su - trainee
 
```

2. Uncomment this line in ***.bashrc*** so ***trainee***'s VM user prompt is ***green*** and distinguishable from VNC user's prompt which is ***yellow***.

```bash
#force_color_prompt
```

3. Create Docker network.

```bash
docker network create --subnet=172.18.0.0/16 rlabs
 
```

4. Run ***Xfce*** VNC so the VM has a UI on port 80 (config is in stage 3).

```bash
docker run --name vanilla-vnc  -d -e VNC_PW=trainee! --restart=always --net rlabs --hostname vnc-terminal.rlabs.org --ip 172.18.0.2 -p 80:6901 consol/ubuntu-xfce-vnc
 
```

5. Run ***Redis Insight*** so students can explore databases in a UI.

```bash
docker run --name insight -d -v redisinsight:/db --restart=always --net rlabs --dns 172.18.0.20 --hostname insight.rlabs.org --ip 172.18.0.4  redislabs/redisinsight
 
```

## Create scripts that run nodes and create clusters 

Students start and stop nodes from the VNC container. Alias commands allow them to transparently SSH to the base VM where scripts run in a controlled manner.

1. Create scripts.

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

2. Start nodes.

```bash
scripts/start_north_nodes.sh
 
```

3. Create a cluster.

```bash
scripts/create_north_cluster.sh
 
```

4. Point your laptop browser to the VM public IP (found in GCP console).

5. Sign in to VNC with password ***trainee!*** .

6. Open Chrome in VNC and point it to ***n1:8443*** .

7. Sign in with ***admin@rlabs.org*** and ***admin*** .

8. Click ***nodes*** to make sure the cluster's running.

9. In GCP shell terminal, stop and remove nodes.

This forces manual restart so clusters build and resolve DNS properly. 

```bash
docker stop n1 n2 n3
docker rm n1 n2 n3
 
```

Now you have:
- Docker
- VNC
- Redis Insight
- Node containers - stopped and removed.

## Save your work

1. Create a snapshot of the VM called ***admin-training-1***.

```bash
gcloud compute disks snapshot admin-training-1 --snapshot-names=admin-training-1 --zone=us-west1-b
 
```
with --labels


2. Create an image from the snapshot called ***admin-training-1***.

```bash
gcloud compute images create admin-training-1 --source-snapshot admin-training-1 --storage-location us-west1
 
```

3. Create an instance template from the image called ***admin-training-1***.

```bash
gcloud compute instance-templates create admin-training-1 \
    --machine-type n1-standard-4 \
    --image-project redislabs-university \
    --image admin-training-1 \
    --network training \
    --subnet training-subnet \
    --region us-west1
 
```

Now you're ready to configure a ***Stage 2 VM***.

```diff
+ Click Next to continue...
```

# >> [Next](../config-vm-stage-2) >>
