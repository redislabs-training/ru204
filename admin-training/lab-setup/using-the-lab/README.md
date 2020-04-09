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

4. On ***workspace 3***, you:
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

13. Navigate to ***Servers > BIND DNS Server***. click the ***rlabs.org*** zone icon at the bottom.

![](img/349-dns-click-rlabs.png)

14. Click ***Edit zone records file*** to view the DNS records.

![](img/350-dns-click-edit-zone.png)

These zone records say, "For URL requests to the domain ***north.rlabs.org*** (your cluster), there are 3 name servers (***n1***, ***n2***, ***n3***) that can provide IPs of proxies listening for databases in that cluster. 

This allows proxies to listen on various nodes and move about as nodes go up or down, databases start or stop, or proxy policies change.

You don't have to change DNS every time that happens. All you supply is the name of your cluster and NS and A records for your nodes.

![](img/351-dns-zone-file.png)

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

## Stop Nodes and Explore Failover

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
 
```
![](img/372-node-fail-cli-connects-no-db-response.png)

5. Return to ***vnc terminal*** and restart node ***n1***.

```bash
start_n1
 
```

Again, you see the node that's started (***n1***) and connection closed to the base VM where this command was run.

![](img/373-node-fail-start-n1.png)

6.

![](img/372-node-fail-start-n1.png)
![](img/373-node-fail-.png)
![](img/374-node-fail-.png)
![](img/375-node-fail-.png)
![](img/376-node-fail-.png)
![](img/377-node-fail-.png)
![](img/378-node-fail-.png)

![](img/129%20-%20step%2029%2C%20restart%20node%201.png)

35.

![](img/130%20-%20step%2030%2C%20relaunch%20terminals%20to%20regain%20node%201's%20tab%20and%20check%20proxy%20and%20db.png)

36.

![](img/131%20-%20step%2031%2C%20connection%20still%20works%2C%20data%20gone.png)

37.

![](img/132%20-%20step%2032%2C%20DNS%20points%20north%20to%20node%202%20proxy.png)

38.

![](img/132%20-%20step%2032%2C%20click%20db%20to%20view%2C%20edit%2C%20or%20delete.png)

39.

![](img/133%20-%20step%2033%2C%20create%20new%20db%20with%202%20master%20shards%20and%202%20replicas.png)

40.

![](img/134%20%3D%20step%2034%2C%20view%20rladmin%2C%20notice%20shard%20placement%2C%201%20proxy%2C%20dense%20setting.png)


41.

![](img/135%20-%20step%2035%2C%20dig%20shows%20node%202%20pDNS%20provides%20DNS%20query%20answer%2C%20where's%20the%20proxy.png)

42.

![](img/136%20-%20step%2036%2C%20cluster%20nslookup%20returns%20pDNS%20answering%20queries%2C%20db%20nslookup%20returns%20proxy%20host%20listening.png)

43.

![](img/137%20-%20step%2037%2C%20need%20redis-port%20in%20db%20client%20connection.png)

44.

![](img/138%20-%20step%2038%2C%20deleted%20db%20repots%20server%20offline%20in%20insight.png)

45.

![](img/139%20-%20step%2039%2C%20no%20client%20connect%20in%20inisght%20with%20FQDN%2C%20no%20pwd.png)

46.

![](img/140%20-%20step%2040%2C%20set%20a%20key%20again.png)

47.

![](img/141%20-%20step%2041%2C%20node%201%20going%20down%2C%20shard%20not%20promoted%20yet.png)

48.

![](img/142%20-%20step%2042%2C%20slave%20shards%20promoted.png)

49.

![](img/143%20-%20step%2043%2C%20data%20still%20in%20promoted%20shards.png)

50.

![](img/144%20-%20step%2044%2C%20restart%20node%201.png)

51.

![](img/145%20-%20step%2045%2C%20node%201%20returns%20quickly%20and%20shards%20restart%20as%20slaves.png)

52.

![](img/146%20-%20step%2046%2C%20stop%20node%202%20with%20master%20shards%20and%20proxy.png)

53.

![](img/148%20-%20step%2048%2C%20node%202%20down%2C%20master%20shards%20back%20on%20node%201%2C%20proxy%20back%20on%20node%201.png)

54.

![](img/149%20-%20step%2049%2C%20stop%202%20nodes%2C%20what%20happens.png)

55.

![](img/150-%20step%2050%2C%20cluster%20down%2C%20now%20what.png)

56.

![](img/151%20-%20step%2051%2C%20proxy%20down.png)

57.

![](img/152%20-%20step%2052%2C%20restart%20nodes%201%20and%202%2C%20now%20what%20happens.png)

58.

![](img/153%20-%20step%2053%2C%20start%20all%20nodes.png)

59.

![](img/154%20-%20step%2054%2C%20re-create%20cluster.png)

60.

![](img/155%20-%20step%2055%2C%20no%20cluster%2C%20no%20dbs.png)

61.

![](img/156%20-%20step%2056%2C%20open%20SSH%20to%20base-vm%20and%20manage%20docker%20containers%20and%20images.png)

