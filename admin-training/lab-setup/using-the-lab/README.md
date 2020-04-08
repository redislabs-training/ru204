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

2. Run the following command to start nodes ***n1***, ***n2***, and ***n3*** (the cluster isn't created yet, only the nodes are started running).

![](img/213-vnc-terminal-start-north-nodes.png)

3. Return to ***workspace 1*** to start connecting nodes in a cluster. Refresh tabs for nodes ***n1***, ***n2***, and ***n3*** (tabs 3, 4, and 5 respectively). 

As nodes start running, tab icons display and pages return ***502 Bad Gateway*** messages.

![](img/32%20-%20tsh%20-%20502%20bad%20gateway%20-%20nodes%20still%20coming%20up.png)

4. Keep refreshing pages. Once running, the node redirects you to its ***Setup*** page where you can add that node to a cluster.

When available, click ***Setup*** in node ***n1***'s tag (tab 3) to create the ***north*** cluster and put node ***n1*** in it.

![](img/308-click-setup-to-create-cluster.png)

5. Node ***n1***'s IP address displays. Make sure ***Create Cluster*** is selected. Enter the cluster's Fully Qualified Domain Name as specified in DNS, which in this case is ***north.rlabs.org***. And click ***Next***.

![](img/309-create-cluster-page.png)

7. You don't have a license so just click ***Next*** to continue. If you had a license, you'd enter its key here.

![](img/310-cluster-key-page.png)

8. Enter admin credentials for the cluster. In this case, enter ***admin@rlabs.org*** and password ***admin***. And click ***Next***.

![](img/311-cluster-admin-creds-page.png)

9. You'll be redirected back to the ***Login*** page. Sign in with cluster credentials you just created.

![](img/312-login-page.png)

10. Now your node is part of a cluster. From here, you can act on the cluster, nodes, or databases.

![](img/313-create-db-prompt.png)

11. Click ***nodes*** to view nodes in the cluster. There is only one so far.

![](img/314-node-list-1-node.png)

12. Add node ***n2*** to the cluster by clicking the second node tab and clicking ***Setup***.

![](img/315-node-2-setup-page.png)

13. Its IP address displays. Click ***Join Cluster*** and enter the IP address of node ***n1*** along with the cluster admin credentials you just created. And click ***Next***.

![](img/316-join-cluster-page.png)

14. Now two nodes are in the cluster.

![](img/317-node-list-2-nodes.png)

15. Add node ***n3*** to the cluster by clicking the third node tab and repeat steps for node ***n2***.

![](img/318-node-list-3-nodes.png)

## Possible Issues:

1. Entering the wrong IP (an unreachable one).

![](img/319-join-cluster-wrong-ip.png)

2. Entering the cluster name, or your own IP, or the wrong credentials.

![](img/320-join-cluster-not-ip-or-wrong-creds.png)

## Check Cluster Status

1. Go to ***workspace 2*** to view more cluster information. Double click the launcher for ***north node CLIs***. The window opens with 3 tabs SSH'd in to the nodes. On node ***n2*** or ***n3***, run ***rladmin status*** to get info on nodes, databases, endpoints, and shards. Right now you don't have any databases, so nothing shows up for databases, endpoints, or shards.

![](img/330-check-rladmin.png)

2. To run DNS tests, go to ***workspace 3***. Return to the ***vnc terminal*** window and enter ***run_dnsutils*** and ***nslookup n1.rlabs.org***. The DNS server is running on ***172.18.0.20***.

![](img/331-check-nslookup-n1.png)

3. Run ***nslookup north.rlabs.org***. You get an authoritative answer from one of the nodes in the ***north*** cluster. In this case, ***n1.rlabs.org***. Run ***nslookup south.rlabs.org***. You get SERVFAIL because the ***south*** cluster isn't running yet and there are no nodes in it to respond.

![](img/332-check-nslookup-north-and-south.png)

## Add a Database

1. Return to node ***n1***'s admin console and click ***databases*** to add a database to the cluster. 

![](img/113%20-%20step%2013%2C%20return%20to%20node%201%20and%20click%20dbs.png)

2. Give it a name and 1 GB of RAM. Enter a password for the database admin (it could be different than the cluster admin). Leave Replication and Persistence disabled for now. Click ***Show advanced options***. 

![](img/115%20-%20step%2015%2C%20enter%20db%20info.png)

21. Enter an endpoint port number between 10000-19999. In this case, enter 12000. Proxies in the cluster will listen for connections on port 12000 for this database. By default, only one proxy starts listening and it's on the node from which you create the database (in this case node ***n1***). Click ***Create*** to create the database (not shown).

![](img/116%20-%20step%2016%2C%20enter%20endpoint%20port%2012000.png)

22. Click the ***configuration*** tab to see database information including its endpoint location and connection URL.

![](img/117%20-%20step%2017%2C%20wait%20for%20db%20and%20endpoint.png)

23. Return to node ***n2*** or ***n3***'s SSH terminal to view updated details of your cluster. Note that you have a database running. It has a single proxy listening on node ***n1***. And it has one shard running on the node where you created the database.

![](img/118%20-%20step%2018%2C%201%20shard%2C%201%20proxy%2C%20on%20node%201.png)

24. Connect to your database using the ***redis-cli*** command line client from any node in your VM (in this case node ***n3***). It's good to test this from a host other than the one the endpoint is listening on to make sure DNS is resolving database and cluster lookups.

NOTE: This example uses simply the cluster name which is not entirely correct. You'll see why shortly.

![](img/119%20-%20step%2019%2C%20db%20connection%20from%20anywhere%20with%20DNS.png)

25. Return to the vnc terminal and run ***dig @ns.rlabs.org north.rlabs.org*** to get more DNS information. Notice that all nodes in the cluster can provide an answers to where the proxy is listening and node ***n1*** provided the answer. It's tempting to think that dig is telling you where the proxy is listening, but it's not. It's telling which node is responding to queries about the cluster ***north.rlabs.org***. In a moment, you'll see how this distincation becomes clearer.

![](img/120%20-%20step%2020%2C%20how%20does%20DNS%20resolve%20north.rlabs.org.png)

26.

![](img/121%20-%20step%2021%2C%20set%20a%20key.png)

27.

![](img/122%20-%20step%2022%2C%20add%20the%20db%20to%20redis%20insight.png)

28.

![](img/123%20-%20step%2023%2C%20connect%20insight%20to%20db.png)

29.

![](img/124%20-%20step%2024%2C%20open%20db%20connection%20in%20insight.png)

30.

![](img/125%20-%20step%2025%2C%20view%20data%20in%20Insight.png)

31.

![](img/126%20-%20step%2026%2C%20click%20CLI%20to%20execute%20Redis%20commands%20in%20Insight.png)

32.

![](img/127%20-%20step%2027%2C%20stop%20n1.png)

33.

![](img/128%20-%20step%2028%2C%20node%20down%2C%20SSH%20tab%20closes%2C%20db%20down%2C%20another%20proxy%20listens.png)

34.

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

