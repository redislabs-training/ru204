# Config DNS - Using Bind DNS

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

5. Click **Servers > BIND DNS Server**
  
6. Select all Existing DNS Zones icons at the bottom (to select, hover over one,  click the top-left box)

![](images/01-dns-delete-default-zones.png)

7. Click **Delete Selected**

8. Click **Return to Zone List**

9. Click **Create Master Zone** and make sure the following are set:
- Domain name / Network: **rlabs.org**
- Master server: **ns.rlabs.org**
- Add NS record for master server: checked
- Email address: **admin@rlabs.org**

![](images/02-dns-create-new-zone.png)

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

![](images/03-dns-zone-record-start.png)

Zone record - AFTER

![](images/04-dns-zone-record-with-origin.png)

13. Click **Save**

14. Click **Apply config** – top-right

![](images/05-dns-apply-config.png)

15. Click **Return to record types**

Notice the domain name at the top and the Address (A) and Name Server (NS) record icons

![](images/06-dns-zone-title.png)

![](images/07-dns-record-icons-start.png)

16. If you lose this page, you can return to it by clicking **Servers > BIND Server** on the left and clicking **rlabs.org master zone** icon at the bottom (shown below):

17. Click the **Address** icon and enter the following A records:

Name | Address
---|---
ns | 172.18.0.20
n1 | 172.18.0.21
n2 | 172.18.0.22
n3 | 172.18.0.23
s1 | 172.18.0.31
s2 | 172.18.0.32
s3 | 172.18.0.33
vnc-terminal | 172.18.0.2
insight | 172.18.0.4
dnsutils | 172.18.0.6

Here's what the final list should look like – notice relative names get automatically replaced with absolute names.

![](images/08-dns-a-record-list.png)

Make sure names and addresses are correct before continuing.

NOTE: If you make a mistake, delete and recreate the **rlabs.org** zone file rather than edit records.

18. Click **Return to record types**

19. Click the **Name Server** icon and add the following NS records:

Name | Name Server
---|---
north | n1
north | n2
north | n3
south | s1
south | s2
south | s3

Here's what the final list should look like – again, relative names automatically get replaced with absolute names.

![](images/09-dns-ns-record-list.png)

20. Click **Return to record types**

You should see the following record counts

![](images/10-dns-record-icons-done.png)

21. Click **Apply config**

22. Click the **rlabs.org** icon at the bottom to return to the domain page.

23. Click the **Edit Zone Records File** icon to view the resulting records file.

Make sure these are correct: 
**$ORIGIN rlabs.org.** - line 2 with ending 'dot'
**@** symbol for SOA record – line 3
NS and A records for the name server – lines 9 and 11

![](images/11-dns-zone-record-long-names.png)

24. You can leave names as absolutes or shorten them to relative names as follows:

![](images/12-dns-done.png)

25. If you shorten names, click **Save** and **Apply config**.

26. Do not edit the SOA record again or change an NS or A record type to another (your config will stop working). If you do by accident, start over.

27. Run the following commands from a VNC terminal shell to test:

```bash
run_dnsutils
nslookup n1.rlabs.org
Nslookup s1.rlabs.org
```

If at any time, you start to get failures, it's best to start over with a new zone file.

