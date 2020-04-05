# Admin Training VM Setup

Here are steps to build the initial training VM image from scratch.

Instructors copy student VMs from this image.

Each VM includes the following as shown:
- VNC access on port 80
- Docker networking
- DNS
- Redis Insight
- 6 RE nodes.
![](img/00-vm-overview.png)

Nodes run in containers, but they look like VMs.

All students need is the VM's public IP and VNC password (provided by instructor).

Here's what the desktop looks like when students sign in.

![](img/01-vnc-overview.png)

Setup is built in two stages:
1. Start Docker/VNC, configure DNS
2. Configure VNC.

For easy re-config, each stage produces a VM image and a Docker image (1 for DNS, 1 for VNC).

Docker images are stored in GCR.

## Stage 1 - Start Docker and VNC, configure DNS

1. Create a VPC in GCP with subnet 172.18.0.0/16 in the region where you want to run VMs.

Requirement | Specification
------------|--------------
Name | ***admin-training-vpc***
Subnet Creation Mode | Custom
Subnet Name | ***admin-training-subnet***
Subnet IP Address Range | 172.18.0.0/16

2. Create a firewall rule that allows ingress on all ports from all sources (0.0.0.0/0) to all targets.
 
3. Create the base VM in the region and VPC where you want to run instances.
  
Requirement  | Specification  
------------ | -------------
Name | ***admin-training-stage-1***
CPU | 4
Memory | 15 GB
OS | Ubuntu 18.04 LTS
Disk | 30 GB
Networking | ***admin-training-vpc***
  
4. SSH to the base VM from GCP console to finish setup.

5. Install vim and add ***trainee*** user to the ***docker*** group so users can start, stop, and SSH to containers.

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

6. Install Docker.

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

7. Run ***sudo visudo*** and add the following line so ***trainee*** can start and stop containers without ***sudo***.

```bash
trainee ALL=(ALL) NOPASSWD:ALL
```


8. Switch to ***trainee*** user to create the Docker network, add scripts, and build the initial VNC Docker image and run it as an unconfigured (vanilla) container.

```bash
sudo su - trainee
 
```

9. Uncomment the line ***#force_color_prompt*** in the user's ***.bashrc*** file. This sets VM user prompt to ***green*** so you can tell it apart from the VNC user (***yellow*** prompt).

10. Generate keys so students can 'silently' SSH from VNC user to base VM user and start/stop/SSH RE nodes. 

```bash
mkdir .ssh
ssh-keygen -q -t rsa -N '' -f .ssh/id_rsa 2>/dev/null <<< y >/dev/null
cp -r .ssh/id_rsa.pub .ssh/authorized_keys 

mkdir vnc_docker
cp -r .ssh/ vnc_docker/ssh 
 
```

11. Create bashrc with aliases to run necessary commands.

```bash
cat << EOF > vnc_docker/bashrc
source \$STARTUPDIR/generate_container_user

export PS1='\e[1;33m\u@\h\e[m:\e[1;34m\w\e[m\$ '

alias create_north_cluster="ssh -t trainee@172.18.0.1 ./scripts/create_north_cluster.sh "
alias create_south_cluster="ssh -t trainee@172.18.0.1 ./scripts/create_south_cluster.sh "

alias run_dnsutils="ssh -t trainee@172.18.0.1 ./scripts/run_dnsutils.sh "

alias run_redis_start="ssh -t trainee@172.18.0.1 docker run -it --name redis -h redis -w / redis bash"
alias run_redis_stop="ssh -t trainee@172.18.0.1 docker container rm \$\(docker container ls -q -f '\''status=exited'\''\)"

alias ssh_base-vm="ssh -t trainee@172.18.0.1"        # only used by admins when building VMs

alias start_north_nodes="ssh -t trainee@172.18.0.1 ./scripts/start_north_nodes.sh "
alias start_south_nodes="ssh -t trainee@172.18.0.1 ./scripts/start_south_nodes.sh "

alias start_n1="ssh -t trainee@172.18.0.1 docker start n1 "
alias start_n2="ssh -t trainee@172.18.0.1 docker start n2 "
alias start_n3="ssh -t trainee@172.18.0.1 docker start n3 "
alias start_s1="ssh -t trainee@172.18.0.1 docker start s1 "
alias start_s2="ssh -t trainee@172.18.0.1 docker start s2 "
alias start_s3="ssh -t trainee@172.18.0.1 docker start s3 "

alias stop_n1="ssh -t trainee@172.18.0.1 docker stop n1 "
alias stop_n2="ssh -t trainee@172.18.0.1 docker stop n2 "
alias stop_n3="ssh -t trainee@172.18.0.1 docker stop n3 "
alias stop_s1="ssh -t trainee@172.18.0.1 docker stop s1 "
alias stop_s2="ssh -t trainee@172.18.0.1 docker stop s2 "
alias stop_s3="ssh -t trainee@172.18.0.1 docker stop s3 "
EOF

mkdir scripts

cat << EOF > scripts/start_north_nodes.sh
docker kill n1; docker rm n1;
docker kill n2; docker rm n2;
docker kill n3; docker rm n3;
docker run --name n1 -d --restart=always --cap-add=ALL --net rlabs --dns 172.18.0.20 --hostname n1.rlabs.org --ip 172.18.0.21 redislabs/redis
docker run --name n2 -d --restart=always --cap-add=ALL --net rlabs --dns 172.18.0.20 --hostname n2.rlabs.org --ip 172.18.0.22 redislabs/redis
docker run --name n3 -d --restart=always --cap-add=ALL --net rlabs --dns 172.18.0.20 --hostname n3.rlabs.org --ip 172.18.0.23 redislabs/redis
docker exec --user root n1 bash -c "iptables -t nat -I PREROUTING -p udp --dport 53 -j REDIRECT --to-ports 5300"
docker exec --user root n2 bash -c "iptables -t nat -I PREROUTING -p udp --dport 53 -j REDIRECT --to-ports 5300"
docker exec --user root n3 bash -c "iptables -t nat -I PREROUTING -p udp --dport 53 -j REDIRECT --to-ports 5300"
sleep 60
EOF

cat << EOF > scripts/start_south_nodes.sh
docker kill s1; docker rm s1;
docker kill s2; docker rm s2;
docker kill s3; docker rm s3;
docker run --name s1 -d --restart=always --cap-add=ALL --net rlabs --dns 172.18.0.20 --hostname s1.rlabs.org --ip 172.18.0.31 redislabs/redis
docker run --name s2 -d --restart=always --cap-add=ALL --net rlabs --dns 172.18.0.20 --hostname s2.rlabs.org --ip 172.18.0.32 redislabs/redis
docker run --name s3 -d --restart=always --cap-add=ALL --net rlabs --dns 172.18.0.20 --hostname s3.rlabs.org --ip 172.18.0.33 redislabs/redis
docker exec --user root s1 bash -c "iptables -t nat -I PREROUTING -p udp --dport 53 -j REDIRECT --to-ports 5300"
docker exec --user root s2 bash -c "iptables -t nat -I PREROUTING -p udp --dport 53 -j REDIRECT --to-ports 5300"
docker exec --user root s3 bash -c "iptables -t nat -I PREROUTING -p udp --dport 53 -j REDIRECT --to-ports 5300"
sleep 60
EOF

cat << EOF > scripts/create_north_cluster.sh
docker exec -it n1 bash -c "/opt/redislabs/bin/rladmin cluster create persistent_path \
        /var/opt/redislabs/persist ephemeral_path /var/opt/redislabs/tmp addr 172.18.0.21 \
        name north.rlabs.org username admin@rlabs.org password admin";

docker exec -it n2 bash -c "/opt/redislabs/bin/rladmin cluster join persistent_path \
        /var/opt/redislabs/persist ephemeral_path /var/opt/redislabs/tmp addr 172.18.0.22 \
        username admin@rlabs.org password admin nodes 172.18.0.21";

docker exec -it n3 bash -c "/opt/redislabs/bin/rladmin cluster join persistent_path \
        /var/opt/redislabs/persist ephemeral_path /var/opt/redislabs/tmp addr 172.18.0.23 \
        username admin@rlabs.org password admin nodes 172.18.0.21";
EOF

cat << EOF > scripts/create_south_cluster.sh
docker exec -it s1 bash -c "/opt/redislabs/bin/rladmin cluster create persistent_path \
        /var/opt/redislabs/persist ephemeral_path /var/opt/redislabs/tmp addr 172.18.0.31 \
        name south.rlabs.org username admin@rlabs.org password admin";
docker exec -it s2 bash -c "/opt/redislabs/bin/rladmin cluster join persistent_path \
        /var/opt/redislabs/persist ephemeral_path /var/opt/redislabs/tmp addr 172.18.0.32 \
        username admin@rlabs.org password admin nodes 172.18.0.31";
docker exec -it s3 bash -c "/opt/redislabs/bin/rladmin cluster join persistent_path \
        /var/opt/redislabs/persist ephemeral_path /var/opt/redislabs/tmp addr 172.18.0.33 \
        username admin@rlabs.org password admin nodes 172.18.0.31";
EOF

cat << EOF > scripts/run_dnsutils.sh
docker kill dnsutils; docker rm dnsutils
docker run --name dnsutils -it --net rlabs --dns 172.18.0.20 --hostname dnsutils.rlabs.org --ip 172.18.0.6 tutum/dnsutils
EOF

# make the scripts executable
chmod 755 scripts/start_north_nodes.sh
chmod 755 scripts/start_south_nodes.sh
chmod 755 scripts/create_north_cluster.sh
chmod 755 scripts/create_south_cluster.sh
chmod 755 scripts/run_dnsutils.sh
 
```

12. Create the Docker network.

```bash
#mkdir resolve
#echo 'nameserver 172.18.0.20' > resolve/resolv.conf

docker network create --subnet=172.18.0.0/16 rlabs
 
```

13. Build the VNC Docker image and run it as a container so the VM has a UI.

```bash
cat << EOF > vnc_docker/Dockerfile
## Custom Dockerfile
FROM consol/ubuntu-xfce-vnc

# Switch to root user to install additional software
USER 0

## Install SSH, DNS Utils, and the VNC user's bashrc and chromium-browser.init
RUN apt update; apt install -y ssh dnsutils;
RUN mkdir /headless/.ssh
COPY ./ssh /headless/.ssh
RUN chown -R 1000 /headless/.ssh/
COPY bashrc /headless/.bashrc
RUN chown -R 1000 /headless/.bashrc

## switch back to default user
USER 1000
EOF

cd vnc_docker
docker build -t vanilla-vnc .

docker run --name vanilla-vnc  -d -e VNC_PW=trainee! --restart=always --net rlabs --hostname vnc-terminal.rlabs.org --ip 172.18.0.2 -p 80:6901  vanilla-vnc
 
```

14. Run Redis Insight as a container so students can view database contents in a UI.

```bash
docker run --name insight -d -v redisinsight:/db --restart=always --net rlabs --dns 172.18.0.20 --hostname insight.rlabs.org --ip 172.18.0.4  redislabs/redisinsight
 
```

15. Run ***BIND DNS*** as a container.

```bash
docker run --name vanilla-dns -d --restart=always --net rlabs --dns 172.18.0.20 --hostname ns.rlabs.org --ip 172.18.0.20 -p 10000:10000/tcp  sameersbn/bind
 
```

Someday, you may use ***CoreDNS*** with Corefile and rlabs.db.

```bash
docker run --name vanilla-dns -d -v /home/trainee/coredns/:/root/ --restart=always --net rlabs --dns 172.18.0.20 --hostname ns.rlabs.org --ip 172.18.0.20  coredns/coredns -conf /root/Corefile
```

### Configure BIND DNS with its UI on VNC desktop.

16. Point your browser to the VM public IP (it's in GCP console).

17. Sign in to VNC with password ***trainee!*** .

18. Open Chrome browser on the VNC desktop.

19. Point it to https://172.18.0.20:10000 (this is BIND's admin console).

20. Sign in with ***root*** and ***password*** .

21. Configure the server using these steps.

![Configure DNS](../dns-config/README.md)

### Test DNS config. If DNS doesn't work, remove the container and try again.

22. From a VNC shell terminal, run the following.

```bash
run_dnsutils
nslookup n1.rlabs.org
nslookup s1.rlabs.org
exit
 
```

23. Start Redis Enterprise nodes.

```bash
start_north_nodes
start_south_nodes
 
```

24. Build the cluster.

```bash
create_north_cluster
 
```

25. Resolve cluster names - they only resolve when you have a cluster.

```bash
run_dnsutils
dig @ns.rlabs.org north.rlabs.org
exit
 
```

### Push DNS changes to a GCR image.

26. Return to SSH from GCP console so you're using your ***GCP account***.

If you run these as ***trainee*** you'll get ***config.json*** errors later when running containers. If that happens, log in as ***root*** and remove ***/home/trainee/.docker/config.json*** .

```bash
# authenticate Docker to GCR
exit
exit
gsutil cp gs://admin-training-bucket/ru-gcr-write-key.json /tmp
cat /tmp/ru-gcr-write-key.json | sudo docker login -u _json_key --password-stdin https://gcr.io

# Commit DNS changes to image, tag it for upload, and push the image.
sudo docker commit vanilla-dns admin-training-dns
sudo docker tag admin-training-dns gcr.io/redislabs-university/admin-training-dns
sudo docker push gcr.io/redislabs-university/admin-training-dns 
 
```

### Reset your VM before saving your work.

27. Replace the ***vanilla-dns*** container with a container called ***configured-dns*** from the GCR iamge. 

```bash
sudo docker stop vanilla-dns
sudo docker rm vanilla-dns
sudo docker rmi sameersbn/bind
sudo docker rmi admin-training-dns

sudo docker run --name configured-dns -d --restart=always --net rlabs --dns 172.18.0.20 --hostname ns.rlabs.org --ip 172.18.0.20 -p 10000:10000/tcp  gcr.io/redislabs-university/admin-training-dns
 
```
28. Stop and remove node containers. Removing them forces manual restart on new VMs. Otherwise, clusters will be misconfigured and cluster names will not resolve by DNS properly.

```bash
sudo docker stop n1 n2 n3 s1 s2 s3
sudo docker rm n1 n2 n3 s1 s2 s3
 
```

29. Return to VNC shell. Remove the ***known_hosts*** file and restart ***north*** nodes.

***known_hosts*** gives ***REMOTE HOST ID HAS CHANGED! Host key verification failed*** errors in new VMs.
And clustered nodes would create improperly configured clusters on startup.

```bash
start_north_nodes
rm /headless/.ssh/known_hosts
 
```

Now you have:
- vanilla VNC
- configured DNS
- Redis Insight
- RE node image, containers stopped and removed.

### Save your work.

29. Create a snapshot of the VM called ***admin-training-stage-1***.

30. Create an image from the snapshot called ***admin-training-stage-1***.





## Stage 2 - Configure VNC

Now you have:
- vanilla VNC
- configured DNS
- Redis Insight
- RE node image, containers stopped and removed.

You'll configure VNC with:
- A background image
- 2 workspaces
- 5 launchers (Chrome and 4 terminal shells).

1. Create a new VM called ***admin-training-stage-2*** from image ***admin-training-stage-1***.

### Configure VNC.

**IMPORTANT:** There is one dependency in the VNC Docker image. It includes the private key for the ***trainee*** user to silently authenticate to the base VM. If you configure a new VM that uses new keys, you must create a new VNC Docker image to match it.

2. Sign in to VNC desktop from your laptop browser with password ***trainee!*** .

3. Open a terminal shell window.

4. Restart RE node containers.

```bash
start_north_nodes
start_south_nodes
 
```

5. Open Chrome browser in VNC and point it to admin consoles:

```bash
https://172.18.0.20:10000
http://insight:8001
https://n1:8443
https://n2:8443
https://n3:8443
https://s1:8443
https://s2:8443
https://s3:8443
```

6. Save tabs as bookmarks.

7. Set pages to open on startup.

8. Follow steps here to set up VNC with background, workspaces, and launchers.

![Configure VNC](../vnc-config/README.md)

### Push the VNC container to a GCR image, then download and test it.

9. SSH to the VM from GCP console so you're using your ***GCP account***.

10. Download the service account key again and authenticate Docker to GCR.

```bash
gsutil cp gs://admin-training-bucket/ru-gcr-write-key.json /tmp/
cat /tmp/ru-gcr-write-key.json | sudo docker login -u _json_key --password-stdin https://gcr.io
 
```

11. Return to VNC terminal.

NOTE: Had to move this up before taking VNC Docker image.

```bash
rm /headless/.ssh/known_hosts
 
```

12. Commit changes and upload to GCR.

```bash
sudo docker commit vanilla-vnc admin-training-vnc
sudo docker tag admin-training-vnc gcr.io/redislabs-university/admin-training-vnc
sudo docker push gcr.io/redislabs-university/admin-training-vnc
 
```

13. Replace with GCR image and test.

```bash
sudo docker stop vanilla-vnc
sudo docker rm vanilla-vnc
sudo docker rmi vanilla-vnc
sudo docker rmi consol/ubuntu-xfce-vnc
sudo docker rmi admin-training-vnc

sudo docker run --name configured-vnc  -d -e VNC_PW=trainee! --restart=always --net rlabs --hostname vnc-terminal.rlabs.org --ip 172.18.0.2 -p 80:6901  gcr.io/redislabs-university/admin-training-vnc
 
```

14. Stop and remove node containers. Removing them forces manual restart on a new VM. Otherwise, nodes will start automatically and create misconfigured clusters with cluster names that won't resolve by DNS properly.

```bash
sudo docker stop n1 n2 n3 s1 s2 s3
sudo docker rm n1 n2 n3 s1 s2 s3
 
```

Now you have:
- configured DNS
- configured VNC
- Redis Insight
- RE node image, containers stopped and removed.

You're ready to create user instances.

### Save your work.

15. Create a snapshot of the VM called ***admin-training-stage-2***.

16. Create an image from the snapshot called ***admin-training-stage-2***.

