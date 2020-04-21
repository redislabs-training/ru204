# Start VMs

```diff
+ Version 2004, Ubuntu 18.04, RedisLabs 5.4
```

If you have access to ***redislabs-university***, start VMs from a ***Stage 3 VM*** image or instance template using one of the methods below.

If you don't have access to ***redislabs-university***, use this image that was exported to GCS instead:

```bash
gs://admin-training-bucket/admin-training-vm-2004***.
```

1. For a few VMs:

```bash
gcloud compute instances create user1 user2 --source-instance-template admin-training-3 --zone=us-west1-b
```

2. For many VMs:

```bash
for i in {1..10} gcloud compute instances create user$i --source-instance-template admin-training-3 --zone=us-west1-b
```

3. For manual start up:
- Go to GCP console, ***VM instances***
- Click ***Create Instance***
- Select ***from image*** or ***from template***
- Choose the following: ***us-west1-b*** zone, ***n1-standard-4*** machine type, ***training*** network.

## To export the image

A ***Stage 3 VM*** image was exported to GCS using the following command as outlined in [Exporting a custom image to Cloud Storage](https://cloud.google.com/compute/docs/images/export-image):

```bash
gcloud compute images export --destination-uri gs://admin-training-bucket/admin-training-vm-2004 --image admin-training-3
```

The command requires:
- ***GCE service account*** with ***editor*** role
- ***CloudBuild API service account*** with ***compute.admin***, ***iam.ServiceAccountUser***,  ***iam.ServiceAccountTokenCreator*** roles.
