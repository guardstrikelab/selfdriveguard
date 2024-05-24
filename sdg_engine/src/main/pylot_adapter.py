import math
import json
from src.main.ads_adapter import AdsAdapter
from src.tools.utils import RepeatedTimer


class PylotAdapter(AdsAdapter):
    def __init__(self, ip, ws_port=9088):
        super().__init__(ip, ws_port)

    def init(self):
        super().init()

    def run(self, adapted_ego, state_callback, trace_callback):
        super().run(adapted_ego, state_callback, trace_callback)

        # debug
        self.adapted_ego.draw_tips()
        self.send_control_message("running!")

        # start to run ego spawn monitor
        def ego_spawn_monitor(rolename, world, on_ego_state_change_callback):
            for actor in world.get_actors():
                if actor.type_id.split(".")[0] == "vehicle":
                    if actor.attributes['role_name'] == rolename:
                        on_ego_state_change_callback("Ready")

        self.ego_spawn_monitor_thread = RepeatedTimer(
            0.1, ego_spawn_monitor, "av_ego", self.adapted_ego.world, self.on_ego_state_change)  # auto starts

        print("Send run command")
        # publish run command
        self.send_control_message("run", {
            "town": self.adapted_ego.world.get_map().name,
            "spawn": {
                "x": self.adapted_ego.start_transform.location.x,
                "y": self.adapted_ego.start_transform.location.y,
                "z": self.adapted_ego.start_transform.location.z,
                "roll": self.adapted_ego.start_transform.rotation.roll,
                "pitch": self.adapted_ego.start_transform.rotation.pitch,
                "yaw": self.adapted_ego.start_transform.rotation.yaw
            },
            "target": {
                "x": self.adapted_ego.target_transform.location.x,
                "y": self.adapted_ego.target_transform.location.y,
                "z": self.adapted_ego.target_transform.location.z
            }
        })
        print("Run command sent")
        print(adapted_ego.info())
        print("[Wait]Initializing Ego...")

    def send_target(self):
        pass

    def stop(self):
        self.send_control_message("stop")
        print("Stop sent")
        if self.ego_spawn_monitor_thread:
            self.ego_spawn_monitor_thread.stop()
        if self.ego_driving_monitor_thread:
            self.ego_driving_monitor_thread.stop()
        if self.ego_reach_monitor_thread:
            self.ego_reach_monitor_thread.stop()
        super().stop()

    def ego_has_spawned(self, rolename="av_ego"):
        # judge whether the EGO has been created
        if self.adapted_ego is None:
            return False
        for actor in self.adapted_ego.world.get_actors():
            if actor.type_id.split(".")[0] == "vehicle":
                if actor.attributes['role_name'] == rolename:
                    self.ego_actor = actor
                    self.adapted_ego.carla_actor = actor
                    return True
        return False

    def on_ego_state_change(self, message):
        if message == "Ready" and self.EGO_LAUNCH_FLAG == False and self.ego_has_spawned():
            self.EGO_LAUNCH_FLAG = True
            self.ego_spawn_monitor_thread.stop()
            self.state_callback("READY")
            # start to run ego driving monitor

            def ego_driving_monitor(ego, start_location, on_ego_state_change_callback):
                current_location = ego.get_location()
                delta_dist = math.sqrt(
                    ((current_location.x-start_location.x)**2)+((current_location.y-start_location.y)**2))
                if delta_dist > 0.5:
                    on_ego_state_change_callback("Driving")

            self.ego_driving_monitor_thread = RepeatedTimer(
                0.5, ego_driving_monitor, self.ego_actor, self.adapted_ego.start_transform.location, self.on_ego_state_change)  # auto starts

        if message == "Driving" and self.TARGET_SEND_FLAG == False and self.EGO_LAUNCH_FLAG == True:
            self.TARGET_SEND_FLAG = True
            self.ego_driving_monitor_thread.stop()
            self.state_callback("DRIVING")
            # start to run ego driving monitor

            def ego_reach_monitor(ego, target_location, on_ego_state_change_callback):
                current_location = ego.get_location()
                delta_dist = math.sqrt(
                    ((current_location.x-target_location.x)**2)+((current_location.y-target_location.y)**2))
                if delta_dist < 5:
                    on_ego_state_change_callback("Stopping")

            self.ego_reach_monitor_thread = RepeatedTimer(
                0.5, ego_reach_monitor, self.ego_actor, self.adapted_ego.target_transform.location, self.on_ego_state_change)  # auto starts

        if message == "Stopping" and self.EGO_REACH_FLAG == False and self.EGO_LAUNCH_FLAG == True and self.TARGET_SEND_FLAG == True:
            self.EGO_REACH_FLAG = True
            self.ego_reach_monitor_thread.stop()
            self.state_callback("STOP")

    # TODO: no trace
    def process_trace_msg(self, message):
        data = message['data']
        data = json.loads(data)
        self.trace_callback(data)
