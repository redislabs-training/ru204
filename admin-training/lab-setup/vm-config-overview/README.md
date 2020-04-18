# VM Setup - Overview

Each VM provides the following. Nodes run in containers, but they look like VMs because they have hostnames and IPs.

All someone needs to use a VM is its public IP and VNC password.

![](../images/00-vm-overview.png)

## Building VMs

VMs are built in stages for easy re-config.

Stages include:
1. Docker, VNC, Insight, node containers
2. DNS config
3. VNC config.

Each stage produces a snapshot, image, and template.

Stages 2 and 3 also produce DNS and VNC Docker images, stored in GCR.

## Getting started

A stage 1 VM needs:
- VPC
- Instance template ***admin-training-0***

1. Create a VPC in GCP with subnet 172.18.0.0/16 in the region where you want to run VMs.

Requirement | Specification
------------|--------------
Name | ***training***
Subnet Creation Mode | Custom
Subnet Name | ***training-subnet***
Subnet IP Address Range | 172.18.0.0/16

2. Create a firewall rule that allows ingress on all ports from all sources (0.0.0.0/0) to all targets.

3. Create an instance template ***admin-training-0*** in the region and subnet where you run instances.
  
Requirement  | Specification  
------------ | -------------
Name | ***admin-training-0***
Machine type | ***n1-standard-4***
Image | ***Ubuntu 18.04 LTS***
Disk size (GB) | ***30***
Network | ***training***
Subnet | ***training-subnet***
Region | ***us-west1***

```bash
gcloud compute instance-templates create admin-training-0 \
    --machine-type n1-standard-4 \
    --image ubuntu-1804-bionic-v20200414 \
    --boot-disk-size 30 \
    --network training \
    --subnet training-subnet \
    --region us-west1
 
```
