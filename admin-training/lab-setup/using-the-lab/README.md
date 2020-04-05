# Using the Lab Environment - Overview

1.

![](img/19%20-%20VNC%20starting%20point.png)

2.

![](img/20%20-%20VNC%20workspace%201%20running.png)

3.

![](img/21%20-%20VNC%20workspace%202%20running.png)

4.

![](img/22%20-%20VNC%20workspace%203%20running.png)

5.

![](img/23%20-%20Node%20down%2C%20re-open%20window.png)

6.

![](img/31%20-%20tsh%20-%20chrome%20-%20nodes%20not%20started.png)

1.

![](img/31%20-%20tsh%20-%20chrome%20page%20and%20tab%20not%20loading%20-%20node%20not%20started.png)

1.

![](img/32%20-%20tsh%20-%20502%20bad%20gateway%20-%20nodes%20still%20coming%20up.png)

1.

![](img/33%20-%20tsh%20-%20nodes%20started%2C%20ready%20to%20cluster.png)

1.

![](img/101%20-%20step%201%2C%20enter%20cluster%20name.png)

1.

![](img/102%20-%20step%202%2C%20enter%20cluster%20credentials.png)

1.

![](img/103%20-%20step%203%2C%20sign%20in%20to%20n1.png)

1.

![](img/104%20-%20step%204%2C%20view%20nodes%20or%20create%20db.png)

1.

![](img/105%20-%20step%205%2C%20only%20one%20node.png)

1.

![](img/106%20-%20step%206%2C%20go%20to%20node%202%20and%20setup.png)

1.

![](img/107%20-%20step%207%2C%20join%20node%202%20to%20cluster.png)

1.

![](img/108%20-%20step%208%2C%20view%20nodes%2C%20now%20there%20are%202.png)

1.

![](img/109%20-%20step%209%2C%20now%20there%20are%203%20nodes.png)

1.

![](img/110%20-%20step%2010%2C%20node%20shell%2C%20run%20rladmin.png)

1.

![](img/111%20-%20step%2011%2C%20run%20dnsutils%2C%20lookup%20node.png)

1.

![](img/112%20-%20step%2012%2C%20nslookup%20returns%20north%20but%20not%20south.png)

1.

![](img/113%20-%20step%2013%2C%20return%20to%20node%201%20and%20click%20dbs.png)

1.

![](img/115%20-%20step%2015%2C%20enter%20db%20info.png)

1.

![](img/116%20-%20step%2016%2C%20enter%20endpoint%20port%2012000.png)

1.

![](img/117%20-%20step%2017%2C%20wait%20for%20db%20and%20endpoint.png)

1.

![](img/118%20-%20step%2018%2C%201%20shard%2C%201%20proxy%2C%20on%20node%201.png)

1.

![](img/119%20-%20step%2019%2C%20db%20connection%20from%20anywhere%20with%20DNS.png)

1.

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

