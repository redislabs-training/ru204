# Start VMs

Start user VMs from a ***Stage 3 VM*** image or instance template.

If you don't have access to them, have someone export the image to a GCS object and use it to start VMs (see below).

Current tech stack is:
---|---
Version | ***2004***
OS | ***Ubuntu 18.04 LTS***
RedisLabs | ***5.4***

## Start VMs

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


## Export image to GCS

Make sure the following are enabled. If not, see [Exporting a custom image to Cloud Storage](https://cloud.google.com/compute/docs/images/export-image) for commands to set them.

1. In the ***API & Service > Library*** page, search for ***cloudbuild*** and make sure its enabled (blue icon).

![](images/01-api-cloudbuild.png) 

2. In the ***IAM*** page, make sure the following roles are set.

***GCE service account*** has ***editor*** role

![](images/02-iam-gce-sa-editor-role.png)

***CloudBuild API service account*** has the following roles:
- ***
- ***iam.ServiceAccountUser***
- ***iam.ServiceAccountTokenCreator***

![](images/03-iam-cloudbuild-sa-roles.png)




