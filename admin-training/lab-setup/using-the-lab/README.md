# Using the Lab

## Use the Desktop

1. You start with a blank desktop, 3 workspaces, and 5 launchers.

![](../../lab-use/img/02-vnc-overview.png)

2. On ***workspace 1***, launch Chrome to work with admin consoles for DNS, Redis Insight, and the Redis Enterprise nodes. Because nodes aren't running yet, icons in node tabs do not display and admin pages on port ***8443*** return errors. When running, you can sign in to admin consoles and configure cluster, nodes, and databases.

![](img/301-launch-chrome.png)

3. On ***workspace 2***, you SSH to node VMs and run commands like ***redis-cli***, ***rladmin***, and ***rlcheck***. Because nodes aren't running yet, shell tabs and SSH connections won't open.

![](img/21%20-%20VNC%20workspace%202%20running.png)

4. When a node goes down, intentional or otherwise, you lose its SSH terminal. After a node restarts, you close and re-open the terminal window containing the shell to see it again.

![](img/23%20-%20Node%20down%2C%20re-open%20window.png)

5. On ***workspace 3***, you:
- Use ***vnc terminal*** to start and stop nodes, create clusters, and run DNS Utils
- Use ***base vm*** to install RE software in one of the labs.

![](img/22%20-%20VNC%20workspace%203%20running.png)

## Create a Cluster

1. Go to ***workspace 3*** and launch the VNC terminal to start running nodes.

![](img/212-vnc-terminal.png)

2. Run the following command to start nodes ***n1***, ***n2***, and ***n3*** (the cluster isn't created yet, only the nodes are started).

![](img/213-vnc-terminal-start-north-nodes.png)

3. Return to ***workspace 1*** to start connecting nodes in a cluster. Refresh tabs for nodes ***n1***, ***n2***, and ***n3*** (tabs 3, 4, and 5). 

As nodes start, icons display in tabs and pages return ***502 Bad Gateway*** errors.

![](img/32%20-%20tsh%20-%20502%20bad%20gateway%20-%20nodes%20still%20coming%20up.png)

4. Keep refreshing pages. Once running, the node redirects you to its ***Setup*** page where you can add that node to a cluster.

5. When available, click ***Setup*** in the node ***n1*** tab (tab 3). 

Here, you create the ***north.rlabs.org*** cluster and add node ***n1*** to it.

![](img/308-click-setup-to-create-cluster.png)

IP address for node ***n1*** displays.

Make sure ***Create Cluster*** is checked.

6. Enter the cluster's Fully Qualified Domain Name ***north.rlabs.org.*** and click ***Next***.

This matches what is set in DNS which you'll see in a minute.

![](img/309-create-cluster-page.png)

7. You don't have a cluster key so just click ***Next***.

If you had a license, you'd enter its key here.

![](img/310-cluster-key-page.png)

8. Enter cluster admin credentials, ***admin@rlabs.org*** and password ***admin***, and click ***Next***.

![](img/311-cluster-admin-creds-page.png)

You'll be redirected back to the ***Login*** page.

9. Sign in with cluster credentials you just created.

![](img/312-login-page.png)

10. Now your node is part of a cluster. From here, you can act on the cluster, nodes, or databases.

![](img/313-create-db-prompt.png)

11. Click ***nodes*** to view nodes in the cluster. There is only one so far.

![](img/314-node-list-1-node.png)

12. Add node ***n2*** to the cluster by clicking its tab and clicking ***Setup***.

![](img/315-node-2-setup-page.png)

Its IP address displays.

13. Click ***Join Cluster***. Enter the node ***n1*** IP address, cluster admin credentials you just created, and click ***Next***.

![](img/316-join-cluster-page.png)

14. Now two nodes are in the cluster.

![](img/317-node-list-2-nodes.png)

15. Add node ***n3*** to the cluster by clicking the third node tab and repeat steps for node ***n2***.

![](img/318-node-list-3-nodes.png)

### Possible Issues to this Point

1. Entering the wrong IP (an unreachable one).

![](img/320-issue-join-cluster-wrong-ip.png)

2. Entering a cluster name, a reachable, but incorrect IP, or wrong credentials.

![](img/321-issue-join-cluster-with-name-or-wrong-creds.png)

3. Spinner keeps spinning in the web page. Admin console session timed-out. Remove ***/#/loading*** from the URL and hit return to get a new sign-in page.

![](img/322-issue-session-timed-out-stuck-loading.png)

### Status Check to this Point

1. Go to ***workspace 2*** and launch ***north node CLIs***.

The window opens with 3 tabs SSH'd in to the nodes.

In node ***n3***, get status on nodes and databases by running:

```bash
rladmin status
```

Right now you don't have any databases, so nothing shows up for databases, endpoints, or shards.

![](img/330-check-rladmin-3-nodes.png)

Explore DNS.

2. Go to ***workspace 3*** and run the following in ***vnc terminal***.

```bash
run_dnsutils
nslookup n1.rlabs.org
```

The DNS server is running on ***172.18.0.20***.

![](img/331-check-nslookup-n1.png)

3. Run

```bash
nslookup north.rlabs.org
nslookup south.rlabs.org
```

nslookup returns an authoritative answer from ***n1*** in the ***north*** cluster.
nslookup returns SERVFAIL for the ***south*** cluster because there aren't any nodes in it to respond yet.

![](img/332-check-nslookup-north-and-south.png)

Now you're ready to add a database to your cluster.

## Add a Database

1. Return to node ***n1***'s admin console and click ***databases***. 

![](img/340-click-dbs.png)

2. Give it a name and 1 GB of RAM. Enter a password for the database admin (it could be different than the cluster admin). 

Leave ***Replication*** and ***Persistence*** disabled for now. 

![](img/341-db-create-page.png)

3. Click ***Show advanced options*** and enter 12000 for the port number.

Proxies listen for connections on this port for this database. By default, only one proxy starts listening and it's on the node where you created the database (in this case node ***n1***). Click ***Activate*** to create the database.

![](img/342-db-show-advanced.png)

4. Click the ***configuration*** tab to see database information including its endpoint location and connection URL.

![](img/343-db-config-tab.png)

5. Return to the node ***n3*** SSH terminal to view updates.

You have a database running. It has a single proxy listening on node ***n1***. And it has one shard running on the node where you created the database.

![](img/344-db-check-rladmin.png)

Connect to your database using ***redis-cli***.

You can run this from anywhere that has DNS resolution to your cluster ***north.rlabs.org***. It's good to test from a host other than the one the endpoint is listening on to make sure DNS is resolving.

6. Run ***redis-cli*** on node ***n3***. 

```bash
redis-cli -p 12000 -h redis-12000.north.rlabs.org
```

![](img/345-db-cli-connect.png)

7. Authenticate with the DB password you provided when you created the database.

```bash
auth admin
```

8. Check to see that you're really connected and authenticated

```bash
keys *
```

9. Set a key and value in the database.

```bash
set hello world
```

![](img/346-db-set-key.png)

Return to ***vnc terminal*** and perform some more DNS checks.

11. Get some information on how DNS resolves the IP to your database proxy.

```bash
dig @ns.rlabs.org redis-12000.north.rlabs.org
```

Nodes run DNS name servers that resolve queries to DB proxies. DNS does not know where proxies are listening, it only knows the nodes.

In this case, node ***n1*** provides the answer. It's tempting to think that dig is telling you where the proxy is listening, but it's not. It's only telling which node is responding to database queries for ***redis-12000.north.rlabs.org***.

![](img/347-db-dig.png)

Check the DNS server to see how records are configured for this cluster. 

12. Go to ***workspace 1*** and open the ***BIND*** tab in Chrome (tab 1) and sign in with credentials: ***root*** and ***password***.

![](img/348-dns-login.png)

13. Navigate to ***Servers > BIND DNS Server*** and click the ***rlabs.org*** zone icon at the bottom.

![](img/349-dns-bind-server-page.png)

14. Click ***Edit zone records file*** to view the DNS records.

![](img/350-dns-click-edit-zone.png)

These zone records say:

"For URL requests to ***north.rlabs.org*** (your cluster), there are 3 name servers (***n1***, ***n2***, ***n3***) who can provide IPs of proxies listening for databases in that cluster." 

![](img/351-dns-zone-file.png)

This allows proxies to listen on various nodes and move about as nodes go up or down, databases start or stop, or proxy policies change.

You don't have to change DNS every time that happens. All you supply is the name of your cluster and NS and A records for your nodes.

### Status Check to this Point

1. Double check you can connecct from anywhere.

Go to ***workspace 1*** and open ***Redis Insight*** in Chrome (tab 2), and click ***Add Redis Database > Add Database***.

![](img/360-insight-add-db.png)

2. Enter a database name (can be anything), host and port, DB password (if given), and click ***Add Redis Database***.

![](img/361-insight-connect-db.png)

3. If connection is successful, the DB icon appears. Click it to connect.

![](img/362-insight-click-db.png)

4. Click ***Browser*** to view and work with DB keys and data.

![](img/363-insight-click-browser.png)

5. Click ***CLI*** to execute Redis commands on the database.

![](img/364-insight-click-cli.png)

You've connected to a DNS-resolvable database by command-line and Insight UI.

Now you're ready to stop nodes and see what happens during failover.

## Stop a Node and Explore Failover

Return to ***vnc terminal*** to stop and restart nodes and see how failover works.

1. In ***vnc terminal***, exit from ***dns_utils***

```bash
exit
```
2. Stop node ***n1***.

```bash
stop_n1
```

You'll see the node that stopped (***n1***) and the connection closed from the base VM where the command was run ***172.18.0.1***.

![](img/370-node-fail-stop-n1.png)

3. Return to ***n3*** SSH terminal on ***workspace 2***. Exit ***redis-cli*** if still connected.

```bash
exit
```

4. Get latest cluster status.

```bash
rladmin status
```

SSH tab to node ***n1*** closes, node ***n1*** is down, proxy on another node (***n2***) starts listening, and the database is down because the only master shard is down with no replica.

![](img/371-node-fail-rladmin-db-down.png)

5. Reconnect to the database with ***redis-cli***

Connection to proxy on node ***n2*** works. But the only master shard that was running is down, without a replica, so no Redis instance replies to requests for data.

```bash
redis-cli -p 12000 -h redis-12000.north.rlabs.org
auth admin
keys *
```
![](img/372-node-fail-cli-connects-no-db-response.png)

5. Return to ***vnc terminal*** and restart node ***n1***.

```bash
start_n1
```

Again, you see the node ***n1*** started and connection closed to the base VM where the command was run.

![](img/380-node-back-start-n1.png)

6. Return to node 3's SSH terminal. Close and re-open the window to regain node 1's tab.

```bash
rladmin status
```

Proxy still listens on node 2 (it did not return to node 1). DB is running, but is there any data?

![](img/381-node-back-db-back.png)

7. Reconnect to ***redis-cli***, authenticate, and list keys. 

```bash
redis-cli -p 12000 -h redis-12000.north.rlabs.org
auth admin
keys *
exit
```

There's no data because there's no DB replication or persistence. When the shard restarts, it's empty.

![](img/383-node-back-no-data.png)


8. Return to ***vnc terminal*** and re-run dig on the database connection.

```bash
dig redis-12000.north.rlabs.org
```

Node 2 answers where proxy listens (which happens to be the same node).

![](img/382-node-back-dig-node-2.png)

Now you're ready to explore a database with more options.

## Add Database Replication and (Shard) Clustering

It's called ***database clustering***, but you're splitting data into a ***shard cluster***.

This allows the database to scale horizontally across nodes for:
- Larger datasets on cheaper hardware
- Faster response times with more Redis instances responding.

Enabling replication and clustering requires 4 shards (2 primaries, 2 replicas). 

Free license only provides 4, so you'll need them all.

First remove the old database.  It's also good to see how to delete a database and what happens.

1. Return to admin console on node ***n1*** in your cluster.

NOTE: It could be any node in your cluster, but be sure to use node ***n1*** for this step. It will point out something very useful in DNS later.

Click ***databases*** and the ***demo-db*** link to view, edit, or delete it.

![](img/390-new-db-select-old.png)

2. Click the ***configuration*** tab, scroll to the bottom, and click ***Delete***.

![](img/391-new-db-delete-old.png)

3. Go to ***Redis Insight***, click the ***Redis Insight*** logo (top-left), and click the old database link.

![](img/391b-new-db-go-to-insight.png)

4. If the server is unreachable, it reports ***server offline***.

![](img/392-new-db-old-db-error-in-insight.png)

5. Return to node 1's admin console where you were before on the ***databases*** tab and click the ***+*** icon to add a new database.

![](img/393-new-db-click-add.png)

6. Click ***Show advanced options*** and enter the following information:

| Field | Value |
|---|---|
| Name | ***another-db*** |
| Memory limit | ***1 GB*** |
| Replication | ***enabled*** |
| Password | ***none - leave it blank*** |
| Database clustering | ***enabled*** |
| Endpoint port number | ***13000*** |

Note the number of shards that will be created (4 total).

![](img/394-new-db-config-page.png)

7. Click ***Activate***.

8. Click the ***databases*** tab and note the status:
- Shards: 2 primary (4 total)
- Replication (R) and shard clustering (C) enabled

![](img/395-new-db-check-status.png)

9. Return to ***workspace 2*** and enter the following in node 3's SSH shell

```bash
rladmin status
```

There are some subtle, but important things to note:
- Under ***Databases***: shards are 2 (primaries), placement in ***dense***, and replication is enabled
- Under ***Endpoints***: the proxy is again listening on node 1 (remmember this, we'll bring it up again in the next step)
- Under ***Shards***: both primaries are on node 1 and both replicas are on node 2 (this is because placement ***dense*** tries to pack the shards in as few of nodes as possible for faster response times with the proxy on the same node)

![](img/396-new-db-rladmin.png)

### Status Check to this Point

1. Return to ***vnc terminal*** on ***workspace 3*** and run the following to find out more about how DNS is behaving.

```bash
run_dnsutils
nslookup north.rlabs.org
nslookup redis-13000.north.rlabs.org
```

What you find is that node 2 is providing answers for proxy IPs.
But the proxy is listening for the database is on node 1.

![](img/398-new-db-nslookup-to-north-and-db.png)

2. Run the following in node 3's SSH terminal to set a database key.

```bash
redis-cli -p 13000 -h redis-13000.north.rlabs.org
set hello world
exit
```

Note, you didn't need to authenticate this time because you didn't set a database password during creation.

![](img/399-new-db-set-key.png)

3. Return to ***Redis Insight*** and connect to the new database (no password). Then you can view the key and value.

![](img/400-new-db-insight-connect.png)


### Possible Issues to this Point

1. If you receive either of the following from ***nslookup*** or ***dig***, you may have not set your port properly

![](img/401-issue-db-port-nslookup-error.png)

![](img/402-issue-db-port-dig-error.png)

2. Check your port setting in ***rlamdin*** or admin console.

![](img/403-issue-db-port-rladmin.png)

![](img/404-issue-db-port-admin-console.png)


## Stop a Node and Explore Failover with Replication and Clustering

1. Return to ***vnc terminal*** and stop node 1.

```bash
stop_n1
```

![](img/370-node-fail-stop-n1.png)

2. Return to node 3's SSH shell and review node, proxy, and database status

```bash
rladmin status
```

Node goes down, proxy migrates, master shards are demoted, and slave shards promote to masters.

This happens almost instantly in production.

![](img/410-node-fail2-node1-down-rladmin.png)


3. Node 1 is down. Replica shards are promoted to primaries on node 2. Replica shards on node 1 are down because the node is down.

![](img/411-node-fail2-rladmin-shards-promoted.png)

4. Connect to ***redis-cli*** on node 3 and notice that data is available because shards are replicated.

![](img/412-node-fail2-cli-data-still-in-db.png)

5. Restart node 1 in ***vnc terminal***.

```bash
start_n1
```

![](img/413-node-back2-start-n1.png)

6. If a failed node with primary shards returns in a given time limit, shards restart as replicas to new primaries on other nodes.

![](img/414-node-back2-rladmin-master-shard-restart.png)

