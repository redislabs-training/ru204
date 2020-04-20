# Config VMs

VMs are built in stages for easy re-config.

Stages include:
1. Docker, VNC, Insight, node containers
2. DNS config
3. VNC config.

Each stage produces an image and template.

Stages 2 and 3 also produce DNS and VNC Docker images, stored in GCR.

## Create a VPC and Base Image

A stage 1 VM needs a VPC and base image.

1. Create the VPC and subnet in a region where you run VMs.

Requirement | Specification
------------|--------------
Name | ***training***
Subnet Creation Mode | Custom
Subnet Name | ***training-subnet***
Subnet IP Address Range | 172.18.0.0/16

2. Create a firewall rule that allows port 80 ingress from all sources (0.0.0.0/0) to all targets.

3. Create an instance template called ***admin-training-0*** in the region and subnet where you run VMs.

```diff
+ Base image runs Ubuntu 18.04 LTS
```

```bash
gcloud compute instance-templates create admin-training-0 \
    --machine-type n1-standard-4 \
    --image-project ubuntu-os-cloud \
    --image ubuntu-1804-bionic-v20200414 \
    --boot-disk-size 30 \
    --network training \
    --subnet training-subnet \
    --region us-west1
```

## Configure a Stage 1 VM

```diff
+ Click next to continue...
```

# >> [Next](config-vm-stage-1) >>

