import roslibpy
import time
import json


def main():
    client = roslibpy.Ros(host='localhost', port=9090)
    client.run()

    talker = roslibpy.Topic(client, '/ros_manager',
                            'std_msgs/String', latch=False)

    state_listener = roslibpy.Topic(client, '/decision_maker/state_msg', 'autoware_msgs/State')

    while True:
        cmd = input(">")

        if cmd == "exit":
            break
        elif cmd == "run":
            data = json.dumps({
                "cmd": cmd,
                # "data": "town:=Town03 spawn_point:=107.89,62.54,0,0,360,360",
                "data":{
                    "town":"Town03",
                    "x":107.89,
                    "y":62.54,
                    "z":0,
                    "roll":0,
                    "pitch":360,
                    "yaw":360
                }
            })
        elif cmd == "target":
            data = json.dumps({
                "cmd": cmd,
                # "data": "{ header: { frame_id: 'base_link' }, pose: { position: { x: 142.897613525, y: -62.6981506348, z: 0 }, orientation: { x: 0, y: 0, z: 0.005, w: 1 } } }",
                "data":{
                    "position":{
                        "x": 142.89,
                        "y":-62.69,
                        "z":0
                    },
                    "orientation":{
                        "x":0,
                        "y":0,
                        "z":0.005
                    }
                }
            })
        else:
            data = json.dumps({
                "cmd": cmd
            })
            print(cmd=="run")

        # Must convert to str!!
        talker.publish(roslibpy.Message({'data': str(data)}))
        print('Sending message...')
        print(data)

    # listener = roslibpy.Topic(client, '/trace', 'std_msgs/String')
    # listener.subscribe(lambda message: print(message['data']))

    # time.sleep(10)

    talker.unadvertise()  # Unregister

    client.terminate()


if __name__ == '__main__':
    main()
