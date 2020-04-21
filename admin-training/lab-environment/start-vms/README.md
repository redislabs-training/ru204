# Start VMs

```diff
+ The latest version is 2004 with Ubuntu 18.04 and RedisLabs 5.6.0-20
```

If you have access to the ***redislabs-university*** GCP project, use a ***Stage 3 VM*** image or instance template with one of the methods below.

If you don't have access to ***redislabs-university***, use this image (which was exported to GCS) instead:

```bash
gs://admin-training-bucket/admin-training-vm-2004
```

1. To start a few VMs (e.g., user, user2), run the following:

```bash
gcloud compute instances create user1 user2 --source-instance-template admin-training-3 --zone=us-west1-b
```

2. To start a larger number of similarly named VMs (e.g. user1-20), run the following:

```bash
for i in {1..20} gcloud compute instances create user$i --source-instance-template admin-training-3 --zone=us-west1-b
```

3. To start VMs manually from GCP console:
- Click ***Create Instance***
- Select ***from image*** or ***from template***
- Choose zone ***us-west1-b***, ***n1-standard-4***, and network ***training***.

Now you're ready to use VMs.

```diff
+ Click Next to continue...
```
# <p align="center"><< [Back](../Overview) <<   . . . .  >> [Next](../use-vms)) >></p>

To export an image to GCS, the following command was used as explained [here](https://cloud.google.com/compute/docs/images/export-image).

```bash
gcloud compute images export --destination-uri gs://admin-training-bucket/admin-training-vm-2004 --image admin-training-3
```

The command requires:
- ***GCE service account*** with ***editor*** role
- ***CloudBuild API service account*** with ***compute.admin***, ***iam.ServiceAccountUser***,  ***iam.ServiceAccountTokenCreator*** roles.
