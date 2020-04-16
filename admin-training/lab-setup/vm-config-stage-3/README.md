# Admin Training VM Setup - Stage 3

Here are steps to configure DNS and generate the admin-training-2 snapshot, image, and template.

You can:
- Use the pre-configure VNC Docker image in GCR as is
- Re-configure the Docker image
- Configure the vanilla VNC image from scratch.

## Create the new VM

1. Open Cloud Shell.

2. Create a new VM from the admin-training-1 instance template.

```bash
gcloud compute instances create admin-training-2 --source-instance-template admin-training-1 --zone=us-west1-b
 
```
## Building from scratch

Students start and stop nodes from the VNC container. Alias commands transparenty SSH them to the base VM and run docker commands from there in a safe and controlled manner.

1. SSH to the VM from GCP console

2. Install SSH.

```bash
sudo docker exec --user root vanilla-vnc bash -c "apt update; apt install -y ssh"
 
```

3. Switch to the ***trainee*** user.

```bash
sudo su - trainee
 
```

4. Generate SSH keys so students can 'silently' SSH from the VNC user to the base VM user.

```bash
ssh-keygen -q -t rsa -N '' -f .ssh/id_rsa 2>/dev/null <<< y >/dev/null
cp -r .ssh/id_rsa.pub .ssh/authorized_keys
 
```

5. Run the following as ***root*** or ***default*** on the container.

```bash
docker exec --user root vanilla-vnc bash -c "mkdir /headless/.ssh"
docker exec --user root vanilla-vnc copy ./ssh /headless/.ssh
docker exec --user root vanilla-vnc bash -c "chown -R 1000 /headless/.ssh"
 
```

6. Copy a new alias file with commands to stop and stop node, ***dnsutils***, and ***Redis OS*** containers.

RUN mkdir /headless/.ssh
COPY ./ssh /headless/.ssh
RUN chown -R 1000 /headless/.ssh/
COPY bashrc /headless/.bashrc
RUN chown -R 1000 /headless/.bashrc




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
