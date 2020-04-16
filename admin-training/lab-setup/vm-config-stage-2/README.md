# Admin Training VM Setup - Stage 2

Here are steps to configure DNS and generate the ***admin-training-2*** snapshot, image, and template.

You can:
- Use the pre-configured DNS Docker image from GCR
- Re-configure the DNS Docker image.

## Create the new VM

1. Open Cloud Shell.

2. Create a new VM from the ***admin-training-1*** instance template.

```bash
gcloud compute instances create admin-training-2 --source-instance-template admin-training-1 --zone=us-west1-b
 
```

## Use the pre-configured DNS Docker image

1. SSH to the VM from GCP console.

2. Stop and remove the vanilla DNS container and images.

```bash
sudo docker stop vanilla-dns
sudo docker rm vanilla-dns
sudo docker rmi sameersbn/bind
 
```

3. Authenticate Docker to GCR. 

***IMPORTANT:*** Use your ***GCP account***. If you run these as ***trainee*** you'll get ***config.json errors*** later when running containers. If that happens, log in as root and remove ***/home/trainee/.docker/config.json*** .

```bash
gsutil cp gs://admin-training-bucket/ru-gcr-write-key.json /tmp
cat /tmp/ru-gcr-write-key.json | sudo docker login -u _json_key --password-stdin https://gcr.io
 
```

4. Run the configured DNS server.

```
sudo docker run --name configured-dns -d --restart=always --net rlabs --dns 172.18.0.20 --hostname ns.rlabs.org --ip 172.18.0.20 -p 10000:10000/tcp  gcr.io/redislabs-university/admin-training-dns
 
```

## Check DNS is working

1. Switch to the ***trainee*** user.

```bash
sudo su - trainee
 
```

2. Download and run DNS Utils

```bash
scripts/run_dnsutils.sh
 
```

3. Check DNS resolves host names.

```
nslookup n1.rlabs.org
nslookup s1.rlabs.org
exit
 
```

4. Create a Redis Enterprise cluster - cluster names only resolve when you have a cluster.

```bash
scripts/start_north_nodes.sh
scripts/create_north_cluster.sh
 
```

5. Check DNS resolves cluster names.

```bash
scripts/run_dnsutils.sh
dig @ns.rlabs.org north.rlabs.org
exit
 
```

## Configure the DNS server

Use these steps if you want to re-configure the DNS Docker image or configure a new DNS server from scratch using the vanilla DNS server.

1. Point your laptop browser to the VM public IP (it's in GCP console).

2. Sign in to VNC with password ***trainee!*** .

3. Open Chrome browser on the VNC desktop.

4. Point it to https://172.18.0.20:10000 (this is ***BIND***'s admin console).

5. Sign in with ***root*** and ***password*** .

6. Configure the server using these steps.

![Configure DNS](../dns-config/README.md)

7. Check DNS is working as described above.

8. Return to your ***GCP acocunt*** (not ***trainee***) and commit your changes to the GCR image

```bash
sudo docker commit configured-dns

```

## Clean up your instance

1. As the ***trainee*** user in GCP shell terminal, stop and remove nodes.

This forces manual restart so clusters build and resolve DNS properly.

```bash
docker stop n1 n2 n3
docker rm n1 n2 n3
 
```

2. Now you have:
- Docker networking
- Configured DNS
- Vanilla VNC
- Redis Insight
- Node containers - stopped and removed.

## Save your work

1. Create a snapshot of the VM called ***admin-training-2***.

2. Create an image from the snapshot called ***admin-training-2***.

3. Create an instance template from the iamge called ***admin-training-2***.