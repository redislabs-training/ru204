# Overview

A finished VM includes the following. 

![](images/00-vm-overview.png)

Nodes run in containers, but they look like VMs because they have hostnames and IPs.

The DNS server resolves node and cluster names.

## VM Login

All someone needs to use a VM is its public IP and VNC password.

![](images/01-vnc-login.png)

VNC desktop runs on port 80, so organization firewalls should not block it.

You may need to start VMs with specific IP or a hostname, and that's easily doable.

This is what the VNC desktop looks like at sign in.

![](images/02-vnc-overview.png)

There are 3 workspaces (i.e. displays) so you can keep lots of windows open and organized.

Launchers (on the left) open windows in specific locations.

If you launch windows on specific workspaces, they won't overlap and all you have to do is switch workspaces to get to everything.

## VNC Terminal

Here's what it looks like when you go to workspace 3 and run ***vnc-terminal***.

![](images/03-vnc-terminal.png)

In ***vnc-terminal*** you can run commands to start and stop RE nodes and create clusters.

Students run ***start_north_nodes*** to start the 3 north nodes (not clustered).

Students create clusters manually. the ***create_north_cluster*** command is used to re-create the cluster.

## Admin Consoles

Here's what it looks like when you go to workspace 1 and run ***Chrome*** browser.

![](images/04-console-login.png)

Students can view the DNS server, Redis Insight, and all 6 node admin consoles.

Tabs open and bookmarks are available.

If nodes are not started, node tabs return errors. If nodes are started, but not clustered, you get the Redis Labs ***Setup*** page.

If nodes are joined in a cluster, you get the Redis Labs ***login*** page (shown above).

To sign-in use ***admin@rlabs.org*** and password ***admin***. These are the cluster credentials used by default in labs and with the ***create_north_cluster*** command.

![](images/05-






## Building VMs

VMs are built in stages for easy re-config.

Stages include:
1. Docker, VNC, Insight, RE node containers
2. DNS config
3. VNC config.

Each stage produces a VM snapshot, image, and template.

Stages 2 and 3 also produce DNS and VNC Docker images, stored in GCR.

## Getting started

A stage 1 VM needs a VPC and an instance template.

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
Image project | ***ubuntu-os-cloud***
Image | ***Ubuntu 18.04 LTS***
Disk size (GB) | ***30***
Network | ***training***
Subnet | ***training-subnet***
Region | ***us-west1***

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
