# VNC Setup Using ConSol/Xfce

Here you set up VNC with background, workspaces, and launchers.

## Initial state

If you haven't done so already, do the following:

1. Sign in to VNC desktop from your laptop browser with password ***trainee!*** .

2. Open a shell terminal.

3. Start RE nodes.

```bash
start_north_nodes
start_south_nodes
 
```

## Set up the background and theme

1. Right click the desktop and choose ***Desktop Settings***.

2. Click the Redis image to set it as the background.

3. Click the ***Icons*** tab.

4. Remove the default icons except Chrome and close the window.

4. Right click the Firefox launcher on the desktop and delete it.

5. Right click the desktop and choose ***Arrange Desktop Icons*** to move Chrome to the top.

6. Right click the desktop and choose ***Applications > Settings > Appearance***

7. Choose ***xfce-4.2*** to change the theme and click ***Close***.

8. Right click the menu bar and remove the following:
- Clock
- User name
- Separator
- Applications button

9. Right click the workspace selector in the menu bar.

10. Decrease the number of workspaces to 3 and name them:
- ***admin UIs***
- ***node terminals***
- ***vnc and base VM***

11. Click ***Close*** to save.

12. Right click the menu bar and choose ***Panel Preferences***.

13. Click ***Appearance***. 

14. Click the ***Items*** tab.

15. Click and drag ***Workspace Switcher*** to the top and click ***Close*** to save.

## Set up Chrome browser

1. Open Chrome browser in VNC.

2. Go to ***Settings*** and set the following.

Feature | Setting
---|---
Show bookmark bar | enabled
Use system title bar and borders | disabled
Default browser | Make Default

3. In the menu bar, right click ***Apps*** and deselect ***Show apps shortcut***.

4. Open tabs to the following.

Accept all conditions so you reach console pages and icons appear in tabs

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

5. Add them as bookmarks to the bookmark bar.

6. Return to ***Settings*** and set these pages to open on startup.

7. Right click the desktop and go to ***Applications > Settings > Preferred Apps***

8. Select Chrome as the default browser and click ***Close*** to save.

## Set up Chrome launcher to open Chrome in the same place every time

1. Right click Chrome launcher and choose ***Edit Launcher***

2. In 'Command' field
- Remove ***U%***
- Add the following so Chrome opens in the same place every time

```bash
--window-position=130,0 --window-size=1150,900 --window-workspace=0 --ignore-certificate-errors -test-type
```

3. Double click the launcher make sure it opens on the first workspace.

## Set up shell terminal launchers

These are for SSH'ing to RE nodes, the VNC shell, and the base VM.

1. Right click the desktop and select ***Create Launcher***

2. Set up the first launcher for north cluster RE nodes as follows:
- Name: ***north node CLIs***
- Command:
```bash
xfce4-terminal --geometry=113x24+130+0 --hide-menubar
--tab -T "n1" -e "bash -c 'ssh -t trainee@172.18.0.1 docker exec -it n1 bash'"
--tab -T "n2" -e "bash -c 'ssh -t trainee@172.18.0.1 docker exec -it n2 bash'"
--tab -T "n3" -e "bash -c 'ssh -t trainee@172.18.0.1 docker exec -it n3 bash'"
```
- Run as terminal: checked
- Icon: click and select ***utilities terminal***

3. Click ***Create***

4. Set up another launcher for south cluster nodes as follows:
- Name: ***south node CLIs***
- Command:
```bash
xfce4-terminal --geometry=113x20+130+520 --hide-menubar
--tab -T "s1" -e "bash -c 'ssh -t trainee@172.18.0.1 docker exec -it s1 bash'"
--tab -T "s2" -e "bash -c 'ssh -t trainee@172.18.0.1 docker exec -it s2 bash'"
--tab -T "s3" -e "bash -c 'ssh -t trainee@172.18.0.1 docker exec -it s3 bash'"
```
- Run as terminal: checked
- Icon: click and select ***utilities terminal***

5. Set up another launcher for the VNC terminal shell as follows:
- Name: ***vnc terminal***
- Command: 
```bash
xfce4-terminal --geometry=113x24+130+0 --hide-menubar
```
- Run as terminal: checked
- Icon: click and select the ***Actions*** drop-down item and ***Refresh***

6. Set up another launcher for the base VM terminal shell as follows:
- Name: ***base VM***
- Command:
```bash
xfce4-terminal --geometry=113x22+130+520 --hide-menubar -e "bash -c 'ssh -t trainee@172.18.0.1'"
```
- Run as terminal: checked
- Icon: click and select ***System Software Installer***

7. Close, re-open, and re-close all launchers windows to make sure they open in the right places and without issues.

8. Return to other instructions to save your VNC setup as a Docker container in GCR.
