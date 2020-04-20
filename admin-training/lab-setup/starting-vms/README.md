# Start VMs

Create user VMs from image or instance template.

Both are named ***admin-training-3*** in the ***redislabs-university*** project.

Tech stack includes:

Resource | Version
---|---
Image | ***2004***
OS | ***Ubuntu 18.04 LTS***
RedisLabs | ***5.4***

They also use two Docker images from GCR (already included):
- ***admin-training-dns***
- ***admin-training-vnc***


## Ways to create VMs

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
