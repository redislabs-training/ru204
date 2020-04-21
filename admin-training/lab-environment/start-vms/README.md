# Start VMs

```diff
+ Version 2004 with Ubuntu 18.04 and RedisLabs 5.4
```

Start VMs from a ***Stage 3 VM*** image or instance template.

```diff
! IMPORTANT
```
If you don't have access, ask someone to export the image to ***GCS*** and use that (see below).

1. When starting in ***redislabs-university*** choose:
- Zone: ***us-west1-b***
- Machine Type: ***n1-standard-4***
- Network: ***training***

2. Run one of the following:

For a few VMS:

```bash
gcloud compute instances create user1 user2 --source-instance-template admin-training-3 --zone=us-west1-b --labels=version=2004,redis=5-4
```

For many VMs:

```bash
for i in {1..10} gcloud compute instances create user$i --source-instance-template admin-training-3 --zone=us-west1-b
```

For manual start up in GCP console:
- Go to ***Compute Engine > VM instances*** and click ***Create Instance***
- Select ***from image*** or ***from template***.

## To export an image to GCS

Run the following:

```bash
gcloud compute images export --destination-uri gs://admin-training-bucket/admin-training-vm-2004 --image admin-training-3
```

```diff
! IMPORTANT
```
The command needs the following:
- ***CloudBuild API*** enabled
- ***GCE service account*** with ***editor*** role
- ***CloudBuild API service account*** with roles ***compute.admin***, ***iam.ServiceAccountUser***,  ***iam.ServiceAccountTokenCreator*

For help, see [Exporting a custom image to Cloud Storage](https://cloud.google.com/compute/docs/images/export-image).
