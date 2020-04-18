# VM Setup - Overview

A finished VM includes the following. 

![](../images/00-vm-overview.png)

Nodes run in containers, but they look like VMs because they have hostnames and IPs.

All someone needs to use a VM is its public IP and VNC password.

## Building VMs

VMs are built in stages for easy re-config.

Stages include:
1. Docker, VNC, Insight, RE node containers
2. DNS config
3. VNC config.

Each stage produces a VM snapshot, image, and template.

Stages 2 and 3 also produce DNS and VNC Docker images, stored in GCR.

## Getting started

A stage 1 VM needs:
- VPC
- base config.

1. Create a VPC with subnet 172.18.0.0/16 in the region where you run VMs.

Requirement | Specification
------------|--------------
Name | ***training***
Subnet Creation Mode | Custom
Subnet Name | ***training-subnet***
Subnet IP Address Range | 172.18.0.0/16

2. Create a firewall rule that allows port 80 ingress from all sources (0.0.0.0/0) to all targets.

3. Create an instance template ***admin-training-0*** in the region and subnet where you run VMs.
  
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
