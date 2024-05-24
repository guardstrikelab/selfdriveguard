import asyncio
import websockets
import json
import os

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

class ControllerServer:
    def __init__(self):
        self.PORT = 9091
        self.start_server = websockets.serve(self.handler, "0.0.0.0", self.PORT)


    async def handler(self,websocket, path):
        async for data in websocket:
            msg = json.loads(data)
            print(msg)
            # print("cmd:{},data:{}".format(msg['cmd'], msg['data']))
            cmd = msg['cmd']
            data = msg['data']
            if cmd == "run":
                os.system("nohup python /home/autoware/my_scripts/trace_generator/src/trace_generator/trace_generator.py >> /home/autoware/trace.log 2>&1 &")
                if os.environ.get("CARLA_SERVER_IP") == None:
                    os.environ["CARLA_SERVER_IP"] = "127.0.0.1"
                launch_cmd = "nohup roslaunch carla_autoware_agent carla_autoware_agent.launch town:={} spawn_point:={},{},{},{},{},{} host:={} >> /home/autoware/launch.log 2>&1 &".format(data['town'],
                                    data['x'],
                                    data['y'],
                                    data['z'],
                                    data['roll'],
                                    data['pitch'],
                                    data['yaw'],
                                    os.environ.get("CARLA_SERVER_IP"))
                # print(launch_cmd)
                os.system(launch_cmd)

            if cmd == "target":
                publish_cmd = "nohup rostopic pub /move_base_simple/goal geometry_msgs/PoseStamped '{{ header: {{ frame_id: {} }}, pose: {{ position: {{ x: {}, y: {}, z: {} }}, orientation: {{ x: {}, y: {}, z: {}, w: {} }} }} }}' >> /home/autoware/launch.log 2>&1 &".format('base_link',
                                    data["position"]["x"],
                                    data["position"]["y"],
                                    data["position"]["z"],
                                    data["orientation"]["x"],
                                    data["orientation"]["y"],
                                    data["orientation"]["z"],
                                    1)
                print(publish_cmd)
                os.system(publish_cmd)
                
            if cmd == "stop":
                os.system("nohup rosnode kill trace_generator >> /home/autoware/kill.log 2>&1 &")
                os.system("nohup rosnode kill carla_ros_bridge >> /home/autoware/kill.log 2>&1 &")
                os.system("nohup rosnode kill vision_darknet_detect >> /home/autoware/kill.log 2>&1 &")


            greeting = json.dumps({"msg":"ojbk"})
            await websocket.send(greeting)

    def start(self):
        print("server start")
        asyncio.get_event_loop().run_until_complete(self.start_server)
        asyncio.get_event_loop().run_forever()
if __name__ == "__main__":
    controller_server = ControllerServer()
    controller_server.start()