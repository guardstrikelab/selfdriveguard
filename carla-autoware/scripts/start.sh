/bin/bash -c -i "nohup roslaunch rosbridge_server rosbridge_websocket.launch >> /home/autoware/rosbridge.log 2>&1 &"

/bin/bash -c -i "python3 /home/autoware/my_scripts/local_controller/local_controller_ws_server.py"