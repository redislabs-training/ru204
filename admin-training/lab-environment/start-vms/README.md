# Start VMs

```diff
+ Version 2004, Ubuntu 18.04, RedisLabs 5.4
```

Start VMs from an ***Stage 3 VM*** image or instance template.

```diff
! IMPORTANT
```
If you don't have access, ask someone to export the image to ***GCS*** and use that (see below).

1. The ***redislabs-univerity*** image requires:
- Zone: ***us-west1-b***
- Machine Type: ***n1-standard-4***
- Network: ***training***

2. Use one of the following methods to start VMs:

For a few VMs:

```bash
gcloud compute instances create user1 user2 --source-instance-template admin-training-3 --zone=us-west1-b --labels=version=2004,redis=5-4
```

For many VMs:

```bash
for i in {1..10} gcloud compute instances create user$i --source-instance-template admin-training-3 --zone=us-west1-b
```

From GCP console:
- Go to ***VM instances***
- Click ***Create Instance***
- Select ***from image*** or ***from template***.

## To export an image to GCS

Run the following:

```bash
gcloud compute images export --destination-uri gs://admin-training-bucket/admin-training-vm-2004 --image admin-training-3
```

```diff
! IMPORTANT
```
The command needs:
- ***GCE service account*** with ***editor*** role
- ***CloudBuild API service account*** with ***compute.admin***, ***iam.ServiceAccountUser***,  ***iam.ServiceAccountTokenCreator*** roles.

For help, see [Exporting a custom image to Cloud Storage](https://cloud.google.com/compute/docs/images/export-image).
