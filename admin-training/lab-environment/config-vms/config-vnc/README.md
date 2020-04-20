# Config VNC - Using Xfce VNC

If you haven't already...

1. Sign in to VNC desktop from your laptop browser with password ***trainee!*** .

2. Open a shell terminal.

3. Start RE nodes.

```bash
start_north_nodes
start_south_nodes
 
```

## Set the background

1. Right click the desktop and set the following.

Item | Action
---|---
Desktop Settings | choose ***Redis*** image
Icons tab | remove all except Chrome
Arrange Desktop Icons | click
Applications > Settings > Appearance | select ***xfce-4.2***
Applications > Settings > Preferred Apps | choose Chrome

2. Delete the Firefox icon.

3. Right click the menu bar and remove ***Clock***, ***User***, ***Separator***, and ***Applications***.

4. Right click the workspace selector in the menu bar and decrease to 3.

5. Right click the menu bar and choose ***Panel Preferences > Appearance > Items*** tab.

6. Move ***Workspace Switcher*** to the top.

## Set up Chrome

1. Open Chrome and set:

Feature | Setting
---|---
Show bookmark bar | enabled
Use system title bar and borders | disabled
Default browser | Make Default

2. Right click menu bar and deselect ***Show apps shortcut***.

3. Open these tabs, accept conditions, bookmark and open on startup.

```bash
https://172.18.0.20:10000
insight:8001
n1:8443
n2:8443
n3:8443
s1:8443
s2:8443
s3:8443
```

## Set Chrome launcher

1. Right click and choose ***Edit Launcher***

2. In ***Command*** field, replace ***U%*** with

```bash
--window-position=130,0 --window-size=1150,900 --window-workspace=0 --ignore-certificate-errors -test-type
```

3. Double click the launcher and make sure it opens on the first workspace.

## Set terminal launchers

1. Right click desktop and select ***Create Launcher***

2. Set the following and click ***Create***.

Feature | Setting
---|---
Name | ***north node CLIs***
Run as terminal | enabled
Icon | set to ***Utilities terminal***

Command:
```bash
xfce4-terminal --geometry=113x24+130+0 --hide-menubar
--tab -T "n1" -e "bash -c 'ssh -t trainee@172.18.0.1 docker exec -it n1 bash'"
--tab -T "n2" -e "bash -c 'ssh -t trainee@172.18.0.1 docker exec -it n2 bash'"
--tab -T "n3" -e "bash -c 'ssh -t trainee@172.18.0.1 docker exec -it n3 bash'"
```

4. Set the following launchers.

Feature | Setting
---|---
Name | ***south node CLIs***
Run as terminal | enabled
Icon | set to ***Utilities terminal***

Command:
```bash
xfce4-terminal --geometry=113x20+130+520 --hide-menubar
--tab -T "s1" -e "bash -c 'ssh -t trainee@172.18.0.1 docker exec -it s1 bash'"
--tab -T "s2" -e "bash -c 'ssh -t trainee@172.18.0.1 docker exec -it s2 bash'"
--tab -T "s3" -e "bash -c 'ssh -t trainee@172.18.0.1 docker exec -it s3 bash'"
```

Feature | Setting
---|---
Name | ***vnc terminal***
Run as terminal | enabled
Icon | set to ***Actions > Refresh***

- Command: 
```bash
xfce4-terminal --geometry=113x24+130+0 --hide-menubar
```

-Feature | Setting
---|---
Name | ***base vm***
Run as terminal | enabled
Icon | set to ***System Software Installer***
- Command:
```bash
xfce4-terminal --geometry=113x22+130+520 --hide-menubar -e "bash -c 'ssh -t trainee@172.18.0.1'"
```

5. Open and close all launchers.

6. Return to other instructions to save setup as a Docker image in GCR.
