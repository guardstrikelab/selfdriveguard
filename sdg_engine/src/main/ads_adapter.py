import websockets
import asyncio
import json

class AdsAdapter():
    def __init__(self, ip, ws_port):
        self.adapted_ego = None
        self.ego_actor = None
        self.state_callback = None
        self.trace_callback = None

        # use websocket to control
        self.ws_uri = "ws://{}:{}".format(ip, ws_port)

    def init(self):
        self.EGO_LAUNCH_FLAG = False
        self.TARGET_SEND_FLAG = False
        self.EGO_REACH_FLAG = False

    def run(self, adapted_ego, state_callback, trace_callback):
        self.adapted_ego = adapted_ego
        self.state_callback = state_callback
        self.trace_callback = trace_callback
        # send run command

    def send_target(self):
        pass

    def stop(self):
        # send stop message

        self.EGO_LAUNCH_FLAG = False
        self.TARGET_SEND_FLAG = False
        self.EGO_REACH_FLAG = False
        self.trace = []

    def on_ego_state_change(self, message):
        pass

    def process_trace_msg(self, message):
        pass

    def ego_has_spawned(self):
        pass

    def send_control_message(self, cmd, data={'data': None}):
        msg = json.dumps(
            {
                "cmd": cmd,
                "data": data
            }
        )
        asyncio.run(self.send_to_ws(msg))

    async def send_to_ws(self, msg):
        # TODO: optimize the call of connect()
        async with websockets.connect(self.ws_uri) as websocket:
            await websocket.send(msg)
            greeting = await websocket.recv()
            greeting = json.loads(greeting)
            print(greeting)