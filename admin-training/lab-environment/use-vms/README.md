# Use VMs

Here's a light intro to using lab VMs.

This introduces you to the following:
- Signing in
- Navigating desktop workspaces
- Starting nodes
- Viewing RL admin console
- Running ***rladmin status***.

For more exploration including clusters, databases, DNS, and node failure, see the link at the bottom.

## First steps users take to access their environment

1. Open a laptop browser and point it to the public IP you were given to work with.

- If you're a student, you get the IP from your instructor.
- If you're an employee spinning up your own instances, you get it from one of two places:

In Admin Console under ***Compute Engine > VM instances***

![](img/210-gcp-vm-ip.png)

or in Cloud Shell after you run gcloud commands.

![](img/211-cloudshell-vm-ip.png)

2. Click in the password box (top-center) and sign in as ***trainee!*** .

![](img/209-vnc-password-box.png)

## Next steps users take to set up their desktop and start using nodes

1. Go to workspace 1

2. Double click the ***vnc terminal*** icon.

This launches an SSH shell where you can start and stop nodes and create clusters.

![](img/212-vnc-terminal.png)

3. Run ***start_north_nodes*** to start nodes ***n1***, ***n2***, and ***n3*** in your environment. 

Each node runs an instance of a Redis Enterprise node. No clusters are created yet.

![](img/213-vnc-terminal-start-north-nodes.png)

4. Go to workspace 2

5. Open Chrome browser. 8 tabs open to admin consoles for:
- DNS server
- Redis Insight
- 3 north nodes
- 3 south nodes.

NOTE: 3 south nodes are not running yet, so their pages return errors.

![](img/214-vnc-chrome-3-nodes-up.png)

6. Click the 3rd tab to view node ***n1***'s ***Setup*** page. It's ready for you to create a cluster and add the node to it. that's ready for you to create a cluster and add the node to it.

7. Go to workspace 2

8. Double click the ***north node CLIs*** icon.

This opens a window with 3 tabs SSH'd in to your 3 north nodes. From here, you can run rladmin to check node and cluster status.

9. Run ***rladmin status*** in any nodes SSH terminal.

You get an error because nodes aren't added to any cluster yet.

Now you're ready to create clusters, add databases, and investigate DNS and explore node failures. 

```diff
+ Click Next to continue...
```
# <p align="center"><< [Back](../start-vms) <<   . . . .  >> [Next](../../lab-setup/using-the-lab) >></p>
