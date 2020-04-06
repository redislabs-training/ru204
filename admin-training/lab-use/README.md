# Lab Use

There are a several types of users:
- Employees who want to learn RE admin
- Instructors who want to teach a class
- Students taking a class.

Here are basic steps for them to start using they're lab environment.

## Here's what users get

Env
<image>

desktop
<image>

Public IP and password

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

