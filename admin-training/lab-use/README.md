# Lab Overview

Running a cluster of RES instances can be done in one of several ways:
- in a group of containers (using Docker, Kubernetes, or a cloud service)
- in a group of VMs.


## Here's what you get

This lab simulates a group of VMs.

It provides the following:
- DNS
- Docker network
- VNC desktop
- Redis Insight
- 6 RES instances, each running in a container, on a single VM.
![](img/00-vm-overview.png)


Benefits are:
- easy startup and shutdown
- simple refresh
- control of DNS, like in an organization.

An environment with machines running:

You can either start some up on your own in GCP or get one from someone else.

To sign on to one, all you need is its public IP address and the VNC password, which is ***trainee!***.

A main desktop to run everything
![](img/02-vnc-overview.png)

The desktop IP and password

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

