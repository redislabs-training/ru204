# Lab Overview

Running a cluster of RE instances can be done in one of several ways:
- in a group of containers (using Docker, Kubernetes, or a cloud service)
- in a group of VMs.

## Here's what you get

This lab simulates a group of VMs with:
- easy startup and shutdown
- simple refresh
- control of DNS.

What you get is a single VM with:
- Desktop access on port 80
- Docker networking
- DNS
- Redis Insight
- 6 RE nodes.
![](img/00-vm-overview.png)

Nodes run in containers, but they look like VMs because they have hostnames, IPs, and DNS resolution.

All a user needs to access a VM is its public IP and password.

Here's what the desktop looks like when you first sign in.

![](img/02-vnc-overview.png)

## How to get a VM

If you're a student, your instructor will provide with a public IP and VNC password.

If you're a Redis Labs employee, with access to start and stop VMs in the ***redislabs-university*** GCP project, you can spin up your own VMs.

There are couple ways to do this.

The simplest way is to copy your VM from ***admin-training-base-image1*** as follows:

1. Point your browser to

```bash
https://console.cloud.google.com/compute/instances/?project=redislabs-university
```

2. Click 
Create Similarr copy the ***glcoud instance create*** command 



2. The next quickest way is to spin up a group of them using


## First steps users take to access their environment

1. Open a laptop browser and point it to the public IP you were given to work with

2. Click in the password box and sign in as ***trainee!***


## Next steps users take to set up their desktop and start using nodes

1. Go to workspace 3

2. Double click the ***vnc terminal*** icon.

This launches an SSH shell where you can start and stop nodes and create clusters.

3. Run ***start_north_nodes*** to start nodes ***n1***, ***n2***, and ***n3*** in your environment.

Each starts a VM with a Redis Enterprise node running. No clusters are created yet.

4. Go to workspace 1

5. Double click the Chrome browser icon.

This launches Chrome with 8 tabs open (and 8 bookmarks) to admin consoles for your:
- DNS server
- Redis Insight
- 3 north nodes
- 3 south nodes.

NOTE: 3 south nodes are not running yet, so their pages return errors.

6. Click the 3rd tab to view node ***n1***'s Setup page that's ready for you to create a cluster and add the node to it.

7. Go to workspace 2

8. Double click the ***north node CLIs*** icon.

This opens a window with 3 tabs SSH'd in to your 3 north nodes. From here, you can run rladmin to check node and cluster status.

9. Run ***rladmin status*** in any nodes SSH terminal.

You get an error because nodes aren't added to any cluster yet.

Now you're ready to create clusters, join nodes, and add databases. 

