# Admin Training VM Setup - Stage 3

Here are steps to configure DNS and generate the ***admin-training-3*** snapshot, image, and template.

You can:
- Use the pre-configure VNC Docker image in GCR as is
- Re-configure the Docker image
- Configure the vanilla VNC image from scratch.

Here's what the new desktop looks like when students sign in.

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

4. Generate SSH keys so students can 'silently' SSH from the container.

```bash
mkdir .ssh
ssh-keygen -q -t rsa -N '' -f .ssh/id_rsa 2>/dev/null <<< y >/dev/null
cp -r .ssh/id_rsa.pub .ssh/authorized_keys
 
```

5. Copy keys to the container with ***default*** user and ***root*** group.

```bash
docker cp .ssh/ vanilla-vnc:/headless
docker exec --user root vanilla-vnc bash -c "chown -R 1000:0 /headless/.ssh/"
```

6. Create ***.bashrc*** with aliases to start and stop containers.

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

7. Copy ***.bashrc*** to the ***default*** user's home directory.

```bash
docker cp vnc-bashrc vanilla-vnc:/headless/.bashrc
docker exec --user root vanilla-vnc bash -c "chown -R 1000:0 /headless/.bashrc"
 
```

8. Sign in to VNC desktop from your laptop browser with password ***trainee!*** .

9. Open a terminal shell window (prompt should be ***yellow*** from the new ***.bashrc*** file).

10. Restart RE node containers.

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

## Saving VNC changes

## 
Now you have:
- Docker networking
- Configured DNS
- Configured VNC
- Redis Insight
- Node containers - stopped and removed.

## Save your work
1. Create a snapshot of the VM called ***admin-training-3***.

2. Create an image from the snapshot called ***admin-training-3***.

3. Create an instance template from the image called ***admin-training-3***.
