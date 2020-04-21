# Start VMs

If you have access to ***redislabs-university*** you can start user VMs from a ***Stage 3 VM*** image or instance template using one of the methods below.

If you don't have access to ***redislabs-university***, use this image instead:

```bash
gs://admin-training-bucket/admin-training-vm-2004***.
```

The latest version ***2004*** includes:
```diff
+ Ubuntu 18.04 and RedisLabs 5.4
```

1. For a few VMs:

```bash
gcloud compute instances create user1 user2 --source-instance-template admin-training-3 --zone=us-west1-b
```

2. For many VMs:

```bash
for i in {1..10} gcloud compute instances create user$i --source-instance-template admin-training-3 --zone=us-west1-b
```

3. For start up in GCP console:
- Go to ***VM instances*** and click ***Create Instance***
- Select ***from image*** or ***from template***
- Choose zone ***us-west1-b***
- If using an image, also choose machine type ***n1-standard-4***, and network ***training***.

## To export an image to GCS

Use this command outlined in [Exporting a custom image to Cloud Storage](https://cloud.google.com/compute/docs/images/export-image):

```bash
gcloud compute images export --destination-uri gs://admin-training-bucket/admin-training-vm-2004 --image admin-training-3
```

The command requires:
- ***GCE service account*** with ***editor*** role
- ***CloudBuild API service account*** with ***compute.admin***, ***iam.ServiceAccountUser***,  ***iam.ServiceAccountTokenCreator*** roles.
