# Start VMs

You start user VMs from ***Stage 3 VM*** image or instance template. Both are named ***admin-training-3*** in the ***redislabs-university*** project.

If you're not in the ***redislabs-university*** project, you need someone to export the ***admin-training-3*** image to a tar.gz object in GCS and use that to start VMs.

Tech stack includes:

Resource | Version
---|---
Image | ***2004***
OS | ***Ubuntu 18.04 LTS***
RedisLabs | ***5.4***

They also use two Docker images from GCR (already included):
- ***admin-training-dns***
- ***admin-training-vnc***


## Ways to start VMs

1. From ***gcloud*** command:

```bash
gcloud compute instances create admin-training-a admin-training-b --source-instance-template admin-training-3 --zone=us-west1-b --labels=version=2004,redis=5-4
 
```

2. From ***gcloud*** command (for a group of similarly named instances, e.g. user1, user2, ...):

```bash
for i in {1..10} gcloud compute instances create user$i --source-instance-template admin-training-3 --zone=us-west1-b
 
```

3. From GCP console, go to Compute Engine > VM instances and click Create Instance.
- Select


## Steps to export an image to GCS

Steps are described in [Exporting a custom image to Cloud Storage](https://cloud.google.com/compute/docs/images/export-image).

1. Make sure ***CloudBuild*** API is enabled for ***redislabs-university*** project.

Search for ***cloudbuild*** in the ***API & Services > Libary*** page. If it's blue, it's enabled.

![](images/01-api-cloudbuild.png) 

If it's gray, enable it with:

```bash
gcloud services enable cloudbuild.googleapis.com
 
```

2. Make sure ***GCE service account*** has ***project editor*** role.

Look in the ***IAM*** page.

![](images/02-iam-gce-sa-editor-role.png)

3. Make sure ***CloudBuild API service account*** has the following roles.
- ***
- ***iam.ServiceAccountUser***
- ***iam.ServiceAccountTokenCreator***

Look in the ***API*** page.

![](images/03-iam-cloudbuild-sa-roles.png)




