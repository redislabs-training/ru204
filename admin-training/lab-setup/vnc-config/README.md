# VNC Setup Using Xfce

Set the display with background image, theme, fewer icons, and fewer menu bar items

1. SSH to the VM from GCP console

2. If you haven't started Consol/Xfce as a container, run the following:
```bash
docker run --name vanilla-vnc  -d -e VNC_PW=trainee! --restart=always --net rlabs --hostname vnc-terminal.rlabs.org --ip 172.18.0.2 -p 80:6901  vanilla-vnc
```

3. Download the Redis Labs background image from GCS

```bash
gsutil cp gs://admin-training-bucket/background-training-classroom.jpg /tmp
```

4. Copy image to the VNC container

```bash
docker cp /tmp/background-training-classroom.jpg vanilla-vnc:/headless/.config
```

5. Open a laptop browser and point it to the VMs public IP

6. Sign in to VNC desktop with password 'trainee!'

7. Right click desktop

8. Choose Desktop Settings and click the image - it will appear as the background

9. Choose the Icons tab and remove default icons except Chrome

10. Right-click desktop to open Applications > Settings > Appearance

11. Choose 'xfce-4.2' to change the theme

12. Right click the menu bar and remove the following:
- Clock
- User name
- Separator
- Applications button

13. Right click the workspace selector in the menu bar

14. Decrease the number to 3 and name the workspaces as:
- admin UIs
- node terminals
- vnc and base VM

Adjust Chrome launcher to open Chrome in the same place every time without warnings or errors and tabs and bookmarks to admin console UIs

1. Right click the desktop and go to Applications > Settings > Preferred Apps

2. Select Chrome as the default browser

3. Right click Chrome launcher and choose Edit Launcher

4. In 'Command' field
- Remove 'U%'
- Add the following so Chrome opens in the same place every time

```bash
--window-position=130,0 --window-size=1150,900 --window-workspace=0 --ignore-certificate-errors -test-type
 
```

5. Double click the launcher to open and adjust Chrome further

6. If RE nodes aren't running, start them. You want admin console icons to load in Chrome tabs and bookmarks.

7. Open the following tabs in order:
```bash
https://172.18.0.20:10000 (dns)
http://insight:8001 (not https:)
https://n1:8443
https://n2:8443
https://n3:8443
https://s1:8443
https://s2:8443
https://s3:8443
```

8. Save each as a bookmark in the bookmark bar

9. Go to Settings > Appearance and set the following:
- Disable 'Use system title bar and borders'
- Enable 'Show bookmarks bar'
- Select Chromium as default browser
- Set current pages to open on start up.

Create 4 terminal window launchers for Redis Enterprise nodes, VNC terminal, and base VM.

1. Right click the desktop and select 'Create Launcher'

2. Set up the first launcher for north cluster RE nodes as follows:
- Name: north node CLIs
- Command:
```bash
xfce4-terminal --geometry=113x24+130+0 --hide-menubar
--tab -T "n1" -e "bash -c 'ssh -t trainee@172.18.0.1 docker exec -it n1 bash'"
--tab -T "n2" -e "bash -c 'ssh -t trainee@172.18.0.1 docker exec -it n2 bash'"
--tab -T "n3" -e "bash -c 'ssh -t trainee@172.18.0.1 docker exec -it n3 bash'"
```
- Run as terminal: checked
- Icon: click and select 'utilities terminal'

3. Click Create

4. Set up another launcher for south cluster nodes as follows:
- Name: south node CLIs
- Command:
```bash
xfce4-terminal --geometry=113x20+130+520 --hide-menubar
--tab -T "s1" -e "bash -c 'ssh -t trainee@172.18.0.1 docker exec -it s1 bash'"
--tab -T "s2" -e "bash -c 'ssh -t trainee@172.18.0.1 docker exec -it s2 bash'"
--tab -T "s3" -e "bash -c 'ssh -t trainee@172.18.0.1 docker exec -it s3 bash'"
```
- Run as terminal: checked
- Icon: click and select 'utilities terminal'

5. Set up another launcher for the VNC terminal shell as follows:
- Name: vnc terminal
- Command: 
```bash
xfce4-terminal --geometry=113x24+130+0 --hide-menubar
```
- Run as terminal: checked
- Icon: click and select the 'Actions' drop-down item and 'Refresh'

6. Set up another launcher for the base VM terminal shell as follows:
- Name: base VM
- Command:
```bash
xfce4-terminal --geometry=113x22+130+520 --hide-menubar -e "bash -c 'ssh -t trainee@172.18.0.1'"
```
- Run as terminal: checked
- Icon: click and select 'System Software Installer'

7. Close, re-open, and re-close all launchers windows to make sure they open in the right places and without issues.

8. Return to other instructions to save your VNC setup as a Docker container in GCR.
