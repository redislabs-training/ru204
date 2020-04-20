# Config VMs

VMs are built in stages for easy re-config.

Stages include:
1. Docker, VNC, Redis Insight, RES
2. DNS config
3. VNC config.

Each stage produces an VM image and optional instance template.

Stages 2 and 3 also produce DNS and VNC Docker images, stored in GCR.

If you want to update a ***Stage 1 VM*** with new OS or Redis:
- Configure a new ***Stage 1 VM***
- Start a ***Stage 2 VM*** and add the DNS Docker image.
- Start a ***Stage 3 VM*** and add the VNC Docker image.

## Start

A ***Stage 1 VM*** needs a VPC and base image.

1. Create a VPC and subnet where VMs run.

Requirement | Specification
------------|--------------
Name | ***training***
Subnet Creation Mode | Custom
Subnet Name | ***training-subnet***
Subnet IP Address Range | 172.18.0.0/16

2. Create a firewall rule that allows port 80 ingress from all sources (0.0.0.0/0) to all targets.

3. Create an instance template called ***admin-training-0***.

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

Now you're ready to configure a ***Stage 1 VM***

```diff
+ Click Next to continue...
```

# >> [Next](config-vm-stage-1) >>

