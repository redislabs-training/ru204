# DNS Config Using Bind DNS

Each student gets a VM with a Docker network and the following containers:
- DNS server
- VNC desktop
- Redis Insight
- 6 Redis Enterprise nodes.

This doc explains how to set up:
- SOA record for 'rlabs.org' domain
- A records for containers
- NS records for clusters 'north' and 'south'.

1. An unconfigured (vanilla) Bind server should be running on the VM as follows:

```bash
docker run --name vanilla-dns -d --restart=always --net rlabs --dns 172.18.0.20 --hostname ns.rlabs.org --ip 172.18.0.20 -p 10000:10000/tcp sameersbn/bind
```

2. Point a laptop browser to the VM public IP and sign in to VNC as **trainee!**

3. Open a VNC browser and point it to https://172.18.0.20:10000 - Bind's UI called WebMin

4. Sign in as **root** and **password**

5. Click **Servers > BIND DNS Server
  
6. Select all Existing DNS Zones icons at the bottom (to select, hover over one,  click the top-left box)

![](img/04%20-%20DNS%20default%20zone%20select.png)

7. Click **Delete Selected

8. Click **Return to Zone List

9. Click **Create Master Zone** and make sure the following are set:
- Domain name / Network: **rlabs.org**
- Master server: **ns.rlabs.org**
- Add NS record for master server: checked
- Email address: **admin@rlabs.org**

![](img/05%20-%20DNS%20zone%20create.png)

10. Click **Create** 

11. Click **Edit Zone Records File**

12. Make the following changes to the file – see before and after images below:
- Line 1: reduce TTL to 60
- Line 2: Insert new line with the following **$ORIGIN** statement to use relative host names – be sure to include ending 'dot':	

```bash
	$ORIGIN rlabs.org.
 
```

- New lines 3 and 9: remove remaining absolute names **.rlabs.org.**

Zone record – BEFORE

![](img/06%20-%20DNS%20zone%20record%20start.png)

Zone record - AFTER

![](img/07%20-%20DNS%20zone%20record%20zone%20set.png)

13. 

