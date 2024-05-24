#!/usr/bin/env python

# WS client example

import asyncio
import websockets
import json

async def hello():
    uri = "ws://localhost:9091"
    async with websockets.connect(uri) as websocket:
        cmd = json.dumps({"cmd":"run"})

        await websocket.send(cmd)
        print(f"> {cmd}")

        greeting = await websocket.recv()
        greeting = json.loads(greeting)
        print(greeting)

# asyncio.get_event_loop().run_until_complete(hello())

async def main():
    uri = "ws://localhost:9091"
    async with websockets.connect(uri) as websocket:

        while True:
            cmd = input(">")

            if cmd == "exit":
                break
            elif cmd == "run":
                request = {
                        "cmd":cmd,
                        "data":{
                        "town":"Town03",
                        "x":107.89,
                        "y":62.54,
                        "z":0,
                        "roll":0,
                        "pitch":360,
                        "yaw":360
                    }
                    }
                

            elif cmd == "target":
                request = {
                        "cmd":cmd,
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
                    }
                
            else:
                request = {
                        "cmd":cmd,
                        "data":""
                    }
                cmd = json.dumps({"cmd":"run"})

            await websocket.send(json.dumps(request))

            greeting = await websocket.recv()
            greeting = json.loads(greeting)
            print(greeting)
        

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
