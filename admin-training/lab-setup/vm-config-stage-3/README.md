# Admin Training Setup - Stage 3

Here are steps to generate stage 3 VM and VNC Docker image.

You can:
- Configure a new Docker image from scratch
- Use the configured VNC Docker image as is
- Re-configure the Docker image.

Here's what the configured VNC desktop looks like when students sign in.

![](../images/02-vnc-overview.png)

## Create the VM

Create a new VM from ***admin-training-2*** image or instance template by gcloud or GCP console.

```bash
gcloud compute instances create admin-training-3 --source-instance-template admin-training-2 --zone=us-west1-b
 
```

## Build the VNC Docker image from scratch

A ***vanilla*** VNC container is running.

Students start and stop nodes from the container. Alias commands allow them to transparently SSH to the base VM and run Docker commands from there in a controlled manner.

### Copy files to the running container

Copy the following:
- SSH
- SSH keys
- ***.bashrc*** with alias commands
- Redis background image.

1. SSH to the VM from GCP console

2. Install SSH on the VNC container.

```bash
sudo docker exec --user root vanilla-vnc bash -c "apt update; apt install -y ssh"
 
```

3. Switch to the ***trainee*** user.

```bash
sudo su - trainee
 
```

4. Generate keys so students can 'silently' SSH from the container.

```bash
mkdir .ssh
ssh-keygen -q -t rsa -N '' -f .ssh/id_rsa 2>/dev/null <<< y >/dev/null
cp -r .ssh/id_rsa.pub .ssh/authorized_keys
 
```

5. Copy keys to the container.

```bash
docker cp .ssh/ vanilla-vnc:/headless
docker exec --user root vanilla-vnc bash -c "chown -R 1000:0 /headless/.ssh/"
 
```

6. Create a new ***.bashrc*** file so students have alias commands.

```bash
cat << EOF > vnc-bashrc
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
 
```

7. Copy ***.bashrc*** to the container.

```bash
docker cp vnc-bashrc vanilla-vnc:/headless/.bashrc
docker exec --user root vanilla-vnc bash -c "chown -R 1000:0 /headless/.bashrc"
 
```

8. Download Redis background image from GCS and copy it to the container.

```bash
gsutil cp gs://admin-training-bucket/background-training-classroom.jpg /tmp
docker cp /tmp/background-training-classroom.jpg vanilla-vnc:/headless/.config
 
```

### Configure the desktop

1. Sign in to VNC desktop from your laptop browser with password ***trainee!*** .

2. Open VNC terminal.

Prompt is ***yellow*** from the new ***.bashrc*** file.

3. Start RE nodes.

When asked to continue to host 172.18.0.1 (base VM), enter ***yes***.

```bash
start_north_nodes
start_south_nodes
 
```

4. Follow these steps to configure the desktop.

![Configure VNC](../vnc-config/README.md)

5. Remove the ***known_hosts*** file.

***known_hosts*** copied to other VMs gives ***REMOTE HOST ID HAS CHANGED!*** and ***Host key verification failed*** errors. 

```bash
rm /headless/.ssh/known_hosts
 
```

### Push ***vanilla*** Docker image changes to GCR

1. Return to VM terminal from GCP console.

2. Exit from ***trainee*** user to return to your ***GCP account***.

```bash
exit
```

3. Authenticate Docker to GCR.

***IMPORTANT:*** Use your ***GCP account***. If you authenticate Docker to GCR as ***trainee*** you'll get ***config.json errors*** later when running containers. If that happens, log in as ***root*** at that time and remove ***/home/trainee/.docker/config.json*** .

```bash
gsutil cp gs://admin-training-bucket/ru-gcr-write-key.json /tmp
cat /tmp/ru-gcr-write-key.json | sudo docker login -u _json_key --password-stdin https://gcr.io
 
```

4. Commit changes and upload to GCR.

```bash
sudo docker commit vanilla-vnc admin-training-vnc
sudo docker tag admin-training-vnc gcr.io/redislabs-university/admin-training-vnc
sudo docker push gcr.io/redislabs-university/admin-training-vnc
 
```

5. Stop and remove vanilla VNC container and images.

```bash
sudo docker stop vanilla-vnc
sudo docker rm vanilla-vnc
sudo docker rmi consol/ubuntu-xfce-vnc
sudo docker rmi admin-training-vnc
 
```

## Use the configured VNC Docker image

1. SSH to the VM from GCP console.

2. Stop and remove vanilla VNC container and images.

```bash
sudo docker stop vanilla-vnc
sudo docker rm vanilla-vnc
sudo docker rmi consol/ubuntu-xfce-vnc
 
```

3. Authenticate Docker to GCR. 

***IMPORTANT:*** Use your ***GCP account***. If you run these as ***trainee*** you'll get ***config.json errors*** later when running containers. If that happens, log in as root at that time and remove ***/home/trainee/.docker/config.json*** .

```bash
gsutil cp gs://admin-training-bucket/ru-gcr-write-key.json /tmp
cat /tmp/ru-gcr-write-key.json | sudo docker login -u _json_key --password-stdin https://gcr.io
 
```

4. Run the configured VNC server.

```
sudo docker run --name configured-vnc  -d -e VNC_PW=trainee! --restart=always --net rlabs --hostname vnc-terminal.rlabs.org --ip 172.18.0.2 -p 80:6901  gcr.io/redislabs-university/admin-training-vnc
 
```

## Update to a ***newer*** configured VNC Docker image from an ***older*** one

This is needed when updating from an older ***configured*** Docker image.

You must generate and save new SSH keys to the new VNC Docker image ***AND A NEW*** VM image.

1. SSH to the VM from GCP console.

2. Switch to the ***trainee*** user.

```bash
sudo su - trainee
 
```
1. Download and run the older ***configured*** VNC Docker image from GCR.

```
sudo docker run --name configured-vnc  -d -e VNC_PW=trainee! --restart=always --net rlabs --hostname vnc-terminal.rlabs.org --ip 172.18.0.2 -p 80:6901  gcr.io/redislabs-university/admin-training-vnc
 
```


3. Generate new keys so students can 'silently' SSH from the container.

***IMPORTANT***: Run this as ***trainee*** user.

```bash
mkdir .ssh
ssh-keygen -q -t rsa -N '' -f .ssh/id_rsa 2>/dev/null <<< y >/dev/null
cp -r .ssh/id_rsa.pub .ssh/authorized_keys
 
```

5. Copy keys to the running container.

```bash
docker cp .ssh/ configured-vnc:/headless
docker exec --user root configured-vnc bash -c "chown -R 1000:0 /headless/.ssh/"
 
```

6. Sign in to VNC desktop with password ***trainee!*** .

7. Open VNC terminal.

8. Start RE nodes.

***IMPORTANT:*** This step must sign you in to the base VM without a password.

```bash
start_north_nodes
 
```

9. Clean up the instance and save changes to the Docker image and new VM.

```bash


## Clean up instance

If you ***CONFIGURED or TESTED*** VNC...

1. Return to the SSH terminal from the GCP console.
 
2. Stop and remove nodes.

This forces manual restart so clusters build and resolve DNS properly.

```bash
docker stop n1 n2 n3 s1 s2 s3
docker rm n1 n2 n3 s1 s2 s3
 
```

3. SSH to VNC terminal and remove ***known_hosts*** file.

***known_hosts*** copied to other VMs gives ***REMOTE HOST ID HAS CHANGED!*** and ***Host key verification failed*** errors. 

```bash
rm /headless/.ssh/known_hosts
 
```

Now you have:
- Configured DNS
- Configured VNC
- Redis Insight
- Node containers - stopped and removed.

You're ready to create user instances.

## Save your work

1. Create a snapshot of the VM called ***admin-training-3***.

2. Create an image from the snapshot called ***admin-training-3***.

3. Create an instance template from the image called ***admin-training-3***.
