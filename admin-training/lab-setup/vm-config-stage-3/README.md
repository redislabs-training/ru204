# Admin Training VM Setup - Stage 3

Here are steps to configure VNC and generate the ***admin-training-3*** VM snapshot, image, and template.

You can:
- Use the pre-configured VNC Docker image in GCR
- Re-configure the Docker image
- Configure the vanilla ***Xfce*** image from scratch.

Here's what the configured VNC desktop looks like when students sign in.

![](img/01-vnc-overview.png)

## Create the new VM

1. Open Cloud Shell.

2. Create a new VM from the admin-training-1 instance template.

```bash
gcloud compute instances create admin-training-2 --source-instance-template admin-training-1 --zone=us-west1-b
 
```

## Building from scratch

Students start and stop nodes from the VNC container. They use alias commands to transparently SSH to the base VM and run Docker commands from there in a safe and controlled manner.

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

6. Create a new ***.bashrc*** for the ***default*** user with aliases to start and stop containers.

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

8. Sign in to VNC desktop from your laptop browser with password ***trainee!*** .

9. Open a shell terminal (prompt is ***yellow*** from the new ***.bashrc*** file).

10. Start RE nodes.

When asked if you want to continue to host 172.18.0.1, enter ***yes*** (this is the base VM IP on the Docker network).

```bash
start_north_nodes
start_south_nodes
 
```

11. Open Chrome browser in VNC and point it to admin consoles:

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

12. Save tabs as bookmarks.

13. Set pages to open on startup.

14. Follow steps here to set up VNC with background, workspaces, and launchers.

![Configure VNC](../vnc-config/README.md)


## Push VNC changes to a GCR image

1. Return to VNC terminal shell. Remove the ***known_hosts*** file.

***known_hosts*** copied to other VMs gives ***REMOTE HOST ID HAS CHANGED!*** and ***Host key verification failed*** errors. 

```bash
rm /headless/.ssh/known_hosts
 
```

2. Return to your GCP SSH terminal.

3. Exit from ***trainee*** user to return to your ***GCP account***.

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

## Use the configured VNC Docker image

1. SSH to the VM from GCP console.

2. If running after configuring from scratch:

Stop and remove the vanilla VNC container and images.

```bash
sudo docker stop vanilla-vnc
sudo docker rm vanilla-vnc
sudo docker rmi consol/ubuntu-xfce-vnc
 
```

3. If running without configuring from scratch:

Authenticate Docker to GCR. 

***IMPORTANT:*** Use your ***GCP account***. If you run these as ***trainee*** you'll get ***config.json errors*** later when running containers. If that happens, log in as root and remove ***/home/trainee/.docker/config.json*** .

```bash
gsutil cp gs://admin-training-bucket/ru-gcr-write-key.json /tmp
cat /tmp/ru-gcr-write-key.json | sudo docker login -u _json_key --password-stdin https://gcr.io
 
```

4. Run the configured VNC server.

```
sudo docker run --name configured-vnc  -d -e VNC_PW=trainee! --restart=always --net rlabs --hostname vnc-terminal.rlabs.org --ip 172.18.0.2 -p 80:6901  gcr.io/redislabs-university/admin-training-vnc
 
```

## Check VNC is working

1. Point your laptop browser to the VM public IP (it's in GCP console).

2. Sign in to VNC with password ***trainee!*** .

3. Go to ***workspace 3*** and run the ***vnc-terminal*** terminal shell.

4. Make sure the prompt is ***yellow*** and aliases work.

```bash
start_north_nodes
 
```

5. Create the ***north*** cluster.

```bash
create_north_cluster
 
```

6. Check ***dnsutils*** is working.

```bash
run_dnsutils
nslookup n1.rlabs.org
dig @ns.rlabs.org north.rlabs.org
exit
 
```

7. Go to ***workspace 1*** and open Chrome browser.

8. Make sure Chrome opens in place with tabs and bookmarks.

9. Go to ***workspace 2*** and launch ***north node CLIs***.

10 Make sure 3 node tabs open and prompts are ***magenta***, ***yellow***, and ***green***, respectively.

## Clean up your instance

1. Return to VNC terminal shell. Remove the ***known_hosts*** file.

***known_hosts*** copied to other VMs gives ***REMOTE HOST ID HAS CHANGED!*** and ***Host key verification failed*** errors. 

```bash
rm /headless/.ssh/known_hosts
 
```
 
2. As ***trainee*** user in the GCP terminal shell, stop and remove nodes.

This forces manual restart so clusters build and resolve DNS properly.

docker stop n1 n2 n3 s1 s2 s3
docker rm n1 n2 n3 s1 s2 s3

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
