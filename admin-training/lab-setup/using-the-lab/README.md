# Using the Lab

## Using the desktop

1. You start with a blank desktop, 3 workspaces, and 5 launchers.

![](img/19%20-%20VNC%20starting%20point.png)

2. On ***workspace 1***, you open Chrome to work with admin consoles for DNS, Redis Insight, and the Redis Enterprise nodes.

![](img/20%20-%20VNC%20workspace%201%20running.png)

3. On ***workspace 2***, you SSH to node VMs and run commands like ***redis-cli***, ***rladmin***, and ***rlcheck***.

![](img/21%20-%20VNC%20workspace%202%20running.png)

4. On ***workspace 3***, you:
- Start and stop nodes, create clusters, and run DNS Utils and Redis OS from the VNC terminal
- And install RE software or inspect Docker containers from the base VM terminal.

![](img/22%20-%20VNC%20workspace%203%20running.png)

5. When an RE node goes down, intentional or otherwise, you lose its SSH terminal. After a node restarts, you can close and re-open the terminal window containing the SSH shell to see it again.

![](img/23%20-%20Node%20down%2C%20re-open%20window.png)

## Getting Started

1. When you first sign in to VNC, nodes aren't running. In the browser, the node's login page on port ***8443*** returns the following message when it's not running.

![](img/31%20-%20tsh%20-%20chrome%20-%20nodes%20not%20started.png)

2. To start running nodes, go to ***workspace 3*** and in the VNC terminal, run the following command to start nodes ***n1***, ***n2***, and ***n3*** (the cluster isn't created yet, only the nodes are started running).

![](img/) <need an image for start_north_nodes>
  
3. To start connecting nodes in a cluster, go to ***workspace 1***, double click the Chrome launcher, and go to one of the first 3 node tabs (tab 3, 4, or 5). When nodes are starting, you get ***502 Bad Gateway*** messages from the ***Login*** page.

![](img/31%20-%20tsh%20-%20chrome%20page%20and%20tab%20not%20loading%20-%20node%20not%20started.png)

4. <not sure what to do with this image>

![](img/32%20-%20tsh%20-%20502%20bad%20gateway%20-%20nodes%20still%20coming%20up.png)

5. When nodes are started, you get the ***Setup*** page and are able to add them to a cluster.

![](img/33%20-%20tsh%20-%20nodes%20started%2C%20ready%20to%20cluster.png)

6. Create the ***north*** cluster by clicking the first node tab (tab 3) for node ***n1***. Its IP address displays. Make sure ***Create Cluster*** is selected. Enter the cluster's Fully Qualified Domain Name as specified in DNS, which in this case is ***north.rlabs.org***. And click ***Next***.

![](img/101%20-%20step%201%2C%20enter%20cluster%20name.png)

7. You don't have a license so just click ***Next*** to continue. If you had a license, you'd enter its key here.

8. Enter admin credentials for the cluster. In this case, enter ***admin@rlabs.org*** and password ***admin***. And click ***Next***.

![](img/102%20-%20step%202%2C%20enter%20cluster%20credentials.png)

9. You'll be redirected back to the ***Login*** page. Sign in with cluster credentials you just created.

![](img/103%20-%20step%203%2C%20sign%20in%20to%20n1.png)

10. Now your node is part of a cluster. From here, you can act on the cluster, nodes, or databases.

![](img/104%20-%20step%204%2C%20view%20nodes%20or%20create%20db.png)

11. Click ***nodes*** to view nodes in the cluster. There is only one so far.

![](img/105%20-%20step%205%2C%20only%20one%20node.png)

12. Add node ***n2*** to the cluster by clicking the second node tab and clicking ***Setup***.

![](img/106%20-%20step%206%2C%20go%20to%20node%202%20and%20setup.png)

13. Its IP address displays. Click ***Join Cluster*** and enter the IP address of node ***n1*** along with the cluster admin credentials you just created. And click ***Next***.

![](img/107%20-%20step%207%2C%20join%20node%202%20to%20cluster.png)

14. Now two nodes are in the cluster.

![](img/108%20-%20step%208%2C%20view%20nodes%2C%20now%20there%20are%202.png)

15. Add node ***n3*** to the cluster by clicking the third node tab and repeat steps for node ***n2***.

![](img/109%20-%20step%209%2C%20now%20there%20are%203%20nodes.png)

16. Go to workspace 2 to view cluster details. Double click the launcher for ***north node CLIs***. The window opens with 3 tabs SSH'd in to the nodes. On node ***n2*** or ***n3***, run ***rladmin status*** to get info on nodes, databases, endpoints, and shards. Right now you don't have any databases, so nothing shows up for databases, endpoints, or shards.

![](img/110%20-%20step%2010%2C%20node%20shell%2C%20run%20rladmin.png)

17. To run DNS tests, go to ***workspace 3***. Return to the ***vnc terminal*** window and enter ***run_dnsutils*** and ***nslookup n1.rlabs.org***. The DNS server is running on ***172.18.0.20***.

![](img/111%20-%20step%2011%2C%20run%20dnsutils%2C%20lookup%20node.png)

18. Run ***nslookup north.rlabs.org***. You get an authoritative answer from one of the nodes in the ***north*** cluster. In this case, ***n1.rlabs.org***. Run ***nslookup south.rlabs.org***. You get SERVFAIL because the ***south*** cluster isn't running yet and there are no nodes in it to respond.

![](img/112%20-%20step%2012%2C%20nslookup%20returns%20north%20but%20not%20south.png)

19. Return to node ***n1***'s admin console and click ***databases*** to add a database to the cluster. Give it a name and 1 GB of RAM. Enter a password for the database admin (it could be different than the cluster admin). Leave Replication and Persistence disabled for now. Click ***Show advanced options***. 

![](img/113%20-%20step%2013%2C%20return%20to%20node%201%20and%20click%20dbs.png)

20. Enter an endpoint port number between 10000-19999. In this case, enter 12000. Proxies in the cluster will listen for connections on port 12000 for this database. By default, only one proxy starts listening and it's on the node from which you create the database (in this case node ***n1***). Click ***Create*** to create the database (not shown).

![](img/115%20-%20step%2015%2C%20enter%20db%20info.png)

21. Click the ***configuration*** tab to see database information including its endpoint location and connection URL.

![](img/116%20-%20step%2016%2C%20enter%20endpoint%20port%2012000.png)

22. Return to node ***n2*** or ***n3***'s SSH terminal to view updated details of your cluster. Note that you have a database running. It has a single proxy listening on node ***n1***. And it has one shard running on the node where you created the database.

![](img/117%20-%20step%2017%2C%20wait%20for%20db%20and%20endpoint.png)

23. Connect to your database using the ***redis-cli*** command line client from any node in your VM (in this case node ***n3***). It's good to test this from a host other than the one the endpoint is listening on to make sure DNS is resolving database and cluster lookups.

NOTE: This example uses simply the cluster name which is not entirely correct. You'll see why shortly.

![](img/118%20-%20step%2018%2C%201%20shard%2C%201%20proxy%2C%20on%20node%201.png)

24. Return to the vnc terminal and run ***dig @ns.rlabs.org north.rlabs.org*** to get more DNS information. Notice that all nodes in the cluster can provide an answers to where the proxy is listening and node ***n1*** provided the answer. It's tempting to think that dig is telling you where the proxy is listening, but it's not. It's telling which node is responding to queries about the cluster ***north.rlabs.org***. In a moment, you'll see how this distincation becomes clearer.

![](img/119%20-%20step%2019%2C%20db%20connection%20from%20anywhere%20with%20DNS.png)

25. 

![](img/120%20-%20step%2020%2C%20how%20does%20DNS%20resolve%20north.rlabs.org.png)

1.

![](img/121%20-%20step%2021%2C%20set%20a%20key.png)

1.

![](img/122%20-%20step%2022%2C%20add%20the%20db%20to%20redis%20insight.png)

1.

![](img/123%20-%20step%2023%2C%20connect%20insight%20to%20db.png)

1.

![](img/124%20-%20step%2024%2C%20open%20db%20connection%20in%20insight.png)

1.

![](img/125%20-%20step%2025%2C%20view%20data%20in%20Insight.png)

1.

![](img/126%20-%20step%2026%2C%20click%20CLI%20to%20execute%20Redis%20commands%20in%20Insight.png)

1.

![](img/127%20-%20step%2027%2C%20stop%20n1.png)

1.

![](img/128%20-%20step%2028%2C%20node%20down%2C%20SSH%20tab%20closes%2C%20db%20down%2C%20another%20proxy%20listens.png)

1.

![](img/129%20-%20step%2029%2C%20restart%20node%201.png)

1.

![](img/130%20-%20step%2030%2C%20relaunch%20terminals%20to%20regain%20node%201's%20tab%20and%20check%20proxy%20and%20db.png)

1.

![](img/131%20-%20step%2031%2C%20connection%20still%20works%2C%20data%20gone.png)

1.

![](img/132%20-%20step%2032%2C%20DNS%20points%20north%20to%20node%202%20proxy.png)

1.

![](img/132%20-%20step%2032%2C%20click%20db%20to%20view%2C%20edit%2C%20or%20delete.png)

1.

![](img/133%20-%20step%2033%2C%20create%20new%20db%20with%202%20master%20shards%20and%202%20replicas.png)

1.

![](img/134%20%3D%20step%2034%2C%20view%20rladmin%2C%20notice%20shard%20placement%2C%201%20proxy%2C%20dense%20setting.png)


1.

![](img/135%20-%20step%2035%2C%20dig%20shows%20node%202%20pDNS%20provides%20DNS%20query%20answer%2C%20where's%20the%20proxy.png)

1.

![](img/136%20-%20step%2036%2C%20cluster%20nslookup%20returns%20pDNS%20answering%20queries%2C%20db%20nslookup%20returns%20proxy%20host%20listening.png)

1.

![](img/137%20-%20step%2037%2C%20need%20redis-port%20in%20db%20client%20connection.png)

1.

![](img/138%20-%20step%2038%2C%20deleted%20db%20repots%20server%20offline%20in%20insight.png)

1.

![](img/139%20-%20step%2039%2C%20no%20client%20connect%20in%20inisght%20with%20FQDN%2C%20no%20pwd.png)

1.

![](img/140%20-%20step%2040%2C%20set%20a%20key%20again.png)

1.

![](img/141%20-%20step%2041%2C%20node%201%20going%20down%2C%20shard%20not%20promoted%20yet.png)

1.

![](img/142%20-%20step%2042%2C%20slave%20shards%20promoted.png)

1.

![](img/143%20-%20step%2043%2C%20data%20still%20in%20promoted%20shards.png)

1.

![](img/144%20-%20step%2044%2C%20restart%20node%201.png)

1.

![](img/145%20-%20step%2045%2C%20node%201%20returns%20quickly%20and%20shards%20restart%20as%20slaves.png)

1.

![](img/146%20-%20step%2046%2C%20stop%20node%202%20with%20master%20shards%20and%20proxy.png)

1.

![](img/148%20-%20step%2048%2C%20node%202%20down%2C%20master%20shards%20back%20on%20node%201%2C%20proxy%20back%20on%20node%201.png)

1.

![](img/149%20-%20step%2049%2C%20stop%202%20nodes%2C%20what%20happens.png)

1.

![](img/150-%20step%2050%2C%20cluster%20down%2C%20now%20what.png)

1.

![](img/151%20-%20step%2051%2C%20proxy%20down.png)

1.

![](img/152%20-%20step%2052%2C%20restart%20nodes%201%20and%202%2C%20now%20what%20happens.png)

1.

![](img/153%20-%20step%2053%2C%20start%20all%20nodes.png)

1.

![](img/154%20-%20step%2054%2C%20re-create%20cluster.png)

1.

![](img/155%20-%20step%2055%2C%20no%20cluster%2C%20no%20dbs.png)

1.

![](img/156%20-%20step%2056%2C%20open%20SSH%20to%20base-vm%20and%20manage%20docker%20containers%20and%20images.png)
