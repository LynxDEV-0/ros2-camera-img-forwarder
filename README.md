1) Open WSL and use the "hostname -I" comand in cli.
2) Replace WSL_IP in "windows/windows-udp-forwarder.py" to yours.
3) Start "windows/windows-udp-forwarder.py" in Windows.
4) Start "ubuntu/wsl-upd-catcher.py" on Ubuntu.
5) Add your recognition parameters to "ubuntu/tracking-ros2.py".
6) Start "ubuntu/tracking-ros2.py" in WSL.
Now you know object coordinats from /camera/tracking_coords topic!
