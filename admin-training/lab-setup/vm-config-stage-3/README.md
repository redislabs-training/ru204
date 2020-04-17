# Admin Training VM Setup - Stage 3

Here are steps to configure VNC and generate the ***admin-training-3*** VM snapshot, image, and template and the ***admin-training-vnc*** Docker image in GCR.

You can:
- Use the pre-configured VNC Docker image in GCR
- Re-configure the Docker image
- Configure the vanilla ***Xfce*** image from scratch.

Here's what the configured VNC desktop looks like when students sign in.

![](../images/02-vnc-overview.png)

## Create the VM

Create a new VM from the ***admin-training-2*** instance template (or image of same name) by gcloud or GCP console.

Steps are for gcloud with instance template:

1. Open Cloud Shell.

2. Create a new VM.

```bash
gcloud compute instances create admin-training-3 --source-instance-template admin-training-2 --zone=us-west1-b
 
```

## Build the VNC Docker image from scratch

Students start and stop nodes from the VNC container. Alias commands allow them to transparently SSH to the base VM and run Docker commands from there in a controlled manner.

1. SSH to the VM from GCP console

2. Install SSH on the vanilla VNC container.

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

6. Create a new ***.bashrc*** file so students will have the alias commands.

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

7. Copy the ***.bashrc*** file to the container.

```bash
docker cp vnc-bashrc vanilla-vnc:/headless/.bashrc
docker exec --user root vanilla-vnc bash -c "chown -R 1000:0 /headless/.bashrc"
 
```

8. Download the Redis Labs background image from GCS and copy it to the container.

```bash
gsutil cp gs://admin-training-bucket/background-training-classroom.jpg /tmp
docker cp /tmp/background-training-classroom.jpg vanilla-vnc:/headless/.config
 
```

9. Sign in to VNC desktop from your laptop browser with password ***trainee!*** .

10. Open VNC terminal.

Prompt is ***yellow*** from the new ***.bashrc*** file.

11. Start RE nodes.

When asked if you want to continue to host 172.18.0.1, enter ***yes***. This is the base VMs IP.

```bash
start_north_nodes
start_south_nodes
 
```

12. Follow steps here to set up VNC with background, workspaces, and launchers.

![Configure VNC](../vnc-config/README.md)


## Push VNC Docker image changes to GCR

1. SSH to VNC terminal.

2. Remove the ***known_hosts*** file.

***known_hosts*** copied to other VMs gives ***REMOTE HOST ID HAS CHANGED!*** and ***Host key verification failed*** errors. 

```bash
rm /headless/.ssh/known_hosts
 
```

3. SSH to VM from GCP console.

4. Exit from ***trainee*** user to return to your ***GCP account***.

```bash
exit
```

4. Authenticate Docker to GCR.

***IMPORTANT:*** Use your ***GCP account***. If you run these as ***trainee*** you'll get ***config.json errors*** later when running containers. If that happens, log in as ***root*** at that time and remove ***/home/trainee/.docker/config.json*** .

```bash
gsutil cp gs://admin-training-bucket/ru-gcr-write-key.json /tmp
cat /tmp/ru-gcr-write-key.json | sudo docker login -u _json_key --password-stdin https://gcr.io
 
```

5. Commit changes and upload to GCR.

```bash
sudo docker commit vanilla-vnc admin-training-vnc
sudo docker tag admin-training-vnc gcr.io/redislabs-university/admin-training-vnc
sudo docker push gcr.io/redislabs-university/admin-training-vnc
 
```

## Use the pre-configured VNC Docker image

1. SSH to the VM from GCP console.

2. Stop and remove vanilla VNC container and images - and ***admin-traininig-vnc*** if you re/configured the image.

```bash
sudo docker stop vanilla-vnc
sudo docker rm vanilla-vnc
sudo docker rmi consol/ubuntu-xfce-vnc
sudo docker rmi admin-training-vnc
 
```

3. Authenticate Docker to GCR. 

***IMPORTANT:*** Use your ***GCP account***. If you run these as ***trainee*** you'll get ***config.json errors*** later when running containers. If that happens, log in as root and remove ***/home/trainee/.docker/config.json*** .

```bash
gsutil cp gs://admin-training-bucket/ru-gcr-write-key.json /tmp
cat /tmp/ru-gcr-write-key.json | sudo docker login -u _json_key --password-stdin https://gcr.io
 
```

4. Run the configured VNC server.

```
sudo docker run --name configured-vnc  -d -e VNC_PW=trainee! --restart=always --net rlabs --hostname vnc-terminal.rlabs.org --ip 172.18.0.2 -p 80:6901  gcr.io/redislabs-university/admin-training-vnc
 
```

## Update to a new VNC Docker image from an old one

This is needed when updating to a new Docker image from an ***older*** one.

You must generate and save new SSH keys to the VNC Docker image and a new VM image.

1. Download and run the older VNC image from GCR.

2. SSH to the VM from GCP console.

2. Switch to the ***trainee*** user.

```bash
sudo su - trainee
 
```
3. Generate new keys so students can 'silently' SSH from the container.

```bash
mkdir .ssh
ssh-keygen -q -t rsa -N '' -f .ssh/id_rsa 2>/dev/null <<< y >/dev/null
cp -r .ssh/id_rsa.pub .ssh/authorized_keys
 
```

5. Copy keys to the ***configured*** container.

```bash
docker cp .ssh/ configured-vnc:/headless
docker exec --user root configured-vnc bash -c "chown -R 1000:0 /headless/.ssh/"
 
```

6. Sign in to VNC desktop from your laptop browser with password ***trainee!*** .

7. Open the VNC terminal.

8. Start RE nodes.

***IMPORTANT:*** This step must silently authenticate you to the base VM and ask if you want to continue connecting to 172.18.0.1. 

```bash
start_north_nodes
 
```

9. Clean up the instance and save changes to the VNC Docker image and a new VM image.

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
