# VM Setup - Stage 2

Generate a Stage 2 VM and DNS Docker image to resolve node and cluster names.

Here's what the BIND DNS zone records look like when done.

![](../images/01-DNS-zone-records-file.png)

## Create new VM and DNS

Create a new VM with a ***vanilla*** BIND DNS server the first time.

1. Create the VM from ***admin-training-1***.

```bash
gcloud compute instances create admin-training-2 --source-instance-template admin-training-1 --zone=us-west1-b
 
```

2. SSH to the VM from GCP console.

3. Run the ***vanilla*** DNS server.

```bash
sudo docker run --name vanilla-dns -d --restart=always --net rlabs --dns 172.18.0.20 --hostname ns.rlabs.org --ip 172.18.0.20 -p 10000:10000/tcp sameersbn/bind
 
```

4. Sign in to VNC desktop from your laptop browser with password ***trainee!*** .

5. Open Chrome on VNC desktop

6. Point it to https://172.18.0.20:10000 (this is ***BIND***'s admin console).

7. Sign in with ***root*** and ***password*** .

8. Configure DNS using these steps.

![Configure DNS](../dns-config/README.md)

9. Check DNS is working.

### Push DNS changes to GCR

1. Return to VM terminal from GCP console.

2. Authenticate Docker to GCR.

```diff
! IMPORTANT
```
Use your ***GCP account***. If you authenticate Docker to GCR as ***trainee*** you'll get ***config.json errors*** later when running containers. If that happens, log in as ***root*** at that time and remove ***/home/trainee/.docker/config.json*** .

```bash
gsutil cp gs://admin-training-bucket/ru-gcr-write-key.json /tmp
cat /tmp/ru-gcr-write-key.json | sudo docker login -u _json_key --password-stdin https://gcr.io
 
```

3. Commit changes and upload DNS Docker image to GCR.

```bash
sudo docker commit vanilla-dns admin-training-dns
sudo docker tag admin-training-dns gcr.io/redislabs-university/admin-training-dns
sudo docker push gcr.io/redislabs-university/admin-training-dns
 
```

4. Stop and remove ***vanilla*** DNS container and images.

```bash
sudo docker stop vanilla-dns
sudo docker rm vanilla-dns
sudo docker rmi sameersbn/bind
sudo docker rmi admin-training-dns
 
```

## Update VM

Update a VM using the ***configured*** DNS Docker image in GCR.

1. Create the VM from ***admin-training-1***.

```bash
gcloud compute instances create admin-training-2 --source-instance-template admin-training-1 --zone=us-west1-b
 
```

2. SSH to the VM from GCP console.

3. Authenticate Docker to GCR.

```diff
! IMPORTANT
```
Use your ***GCP account***. If you authenticate Docker to GCR as ***trainee*** you'll get ***config.json errors*** later when running containers. If that happens, log in as ***root*** at that time and remove ***/home/trainee/.docker/config.json*** .

```bash
gsutil cp gs://admin-training-bucket/ru-gcr-write-key.json /tmp
cat /tmp/ru-gcr-write-key.json | sudo docker login -u _json_key --password-stdin https://gcr.io
 
```

4. Run the ***configured*** DNS server.

```
sudo docker run --name configured-dns -d --restart=always --net rlabs --dns 172.18.0.20 --hostname ns.rlabs.org --ip 172.18.0.20 -p 10000:10000/tcp  gcr.io/redislabs-university/admin-training-dns
 
```

4. Check DNS is working


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

## Configure the DNS server from scratch

Use these steps if you want to re-configure the DNS Docker image or configure a new DNS server from scratch using the vanilla DNS server.

1. SSH to the VM from GCP console.

If configuring from scratch...

Run a ***vanilla*** BIND DNS server.

```bash
sudo docker run --name vanilla-dns -d --restart=always --net rlabs --dns 172.18.0.20 --hostname ns.rlabs.org --ip 172.18.0.20 -p 10000:10000/tcp  sameersbn/bind
 
```

If re-configuring the DNS Docker image in GCR use steps above to remove the


```bash
docker run --name vanilla-dns -d --restart=always --net rlabs --dns 172.18.0.20 --hostname ns.rlabs.org --ip 172.18.0.20 -p 10000:10000/tcp  sameersbn/bind
 
```

4. Point it to https://172.18.0.20:10000 (this is ***BIND***'s admin console).

5. Sign in with ***root*** and ***password*** .



1. Point your laptop browser to the VM public IP (it's in GCP console).

2. Sign in to VNC with password ***trainee!*** .

3. Open Chrome browser on the VNC desktop.

4. Point it to https://172.18.0.20:10000 (this is ***BIND***'s admin console).

5. Sign in with ***root*** and ***password*** .

6. Configure the server using these steps.

![Configure DNS](../dns-config/README.md)

7. Check DNS is working as described above.

8. Return to your ***GCP acocunt*** (not ***trainee***).

9. Commit your changes and upload to GCR.

If a re-config.

```bash
sudo docker commit configured-dns
sudo docker tag configured-dns gcr.io/redislabs-university/admin-training-dns
sudo docker push gcr.io/redislabs-university/admin-training-dns
 
```

## Clean up your instance

1. As the ***trainee*** user in GCP shell terminal, stop and remove nodes.

This forces manual restart so clusters build and resolve DNS properly.

```bash
docker stop n1 n2 n3
docker rm n1 n2 n3
 
```

Now you have:
- Configured DNS
- Vanilla VNC
- Redis Insight
- Node containers - stopped and removed.

## Save your work

1. Create a snapshot of the VM called ***admin-training-2***.

```bash
gcloud compute disks snapshot admin-training-2 --snapshot-names=admin-training-2 --zone=us-west1-b
 
```

2. Create an image from the snapshot called ***admin-training-2***.

```bash
gcloud compute images create admin-training-2 --source-snapshot admin-training-2 --storage-location us-west1
 
```

3. Create an instance template from the iamge called ***admin-training-2***.

```bash
gcloud compute instance-templates create admin-training-2 \
    --machine-type n1-standard-4 \
    --image-project redislabs-university \
    --image admin-training-2 \
    --network training \
    --subnet training-subnet \
    --region us-west1
 
```

```diff
! SKIP
```
Someday, you may want to use ***CoreDNS*** with Corefile and rlabs.db.

```bash
docker run --name vanilla-dns -d -v /home/trainee/coredns/:/root/ --restart=always --net rlabs --dns 172.18.0.20 --hostname ns.rlabs.org --ip 172.18.0.20  coredns/coredns -conf /root/Corefile
```
