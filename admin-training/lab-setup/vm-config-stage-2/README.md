# Admin Training VM Setup - Stage 2

Here are steps to configure DNS and generate the ***admin-training-2*** snapshot, image, and template.

You can use these steps to:
- Run the pre-configured DNS Docker image from GCR
- Re-configure the DNS Docker image
- Configure a new DNS server from scratch using the vanilla DNS server.

## Create the new VM

1. Open Cloud Shell.

2. Create a new VM from the ***admin-training-1*** instance template.

```bash
gcloud compute instances create admin-training-2 --source-instance-template admin-training-1 --zone=us-west1-b
 
```

## Get the configured DNS Docker image

1. SSH to the VM from GCP console.

2. Stop and remove the vanilla DNS container and images.

```bash
sudo docker stop vanilla-dns
sudo docker rm vanilla-dns
sudo docker rmi vanilla-dns
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

Use these steps to:
- Re-configure the DNS Docker image
- Configure a new DNS server from scratch using the vanilla DNS server.

1. Point your laptop browser to the VM public IP (it's in GCP console).

2. Sign in to VNC with password ***trainee!*** .

3. Open Chrome browser on the VNC desktop.

4. Point it to https://172.18.0.20:10000 (this is ***BIND***'s admin console).

5. Sign in with ***root*** and ***password*** .

6. Configure the server using these steps.

![Configure DNS](../dns-config/README.md)

7. Check DNS is working as described above.

## Save your changes
