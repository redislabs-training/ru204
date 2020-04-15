# Reconfigure VM Stage 2

This configuration assumes:
- If you need to reconfigure VNC is some way, you had to recreate Stage 1 so it
- As a result, you had to create a new SSH key pair during VM Stage 1 setup

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

## Configure VNC.

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
