import roslaunch
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
import json
import thread
import os

class LocalController:
    def __init__(self):
        self.publisher = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=10)

    def launch(self):
        self.parent.start()

    def callback(self,data):
        data = json.loads(data.data)
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data)
        if data['cmd'] == "run":
            rospy.loginfo("RUN!!!")
            os.system("nohup python /home/autoware/my_scripts/trace_generator/src/trace_generator/trace_generator.py >> /home/autoware/trace.log 2>&1 &")
            launch_cmd = "nohup roslaunch carla_autoware_agent carla_autoware_agent.launch town:={} spawn_point:={},{},{},{},{},{} >> /home/autoware/launch.log 2>&1 &".format(data['data']['town'],
                                data['data']['x'],
                                data['data']['y'],
                                data['data']['z'],
                                data['data']['roll'],
                                data['data']['pitch'],
                                data['data']['yaw'])
            print(launch_cmd)
            os.system("nohup roslaunch carla_autoware_agent carla_autoware_agent.launch town:={} spawn_point:={},{},{},{},{},{} >> /home/autoware/launch.log 2>&1 &"
                        .format(data['data']['town'],
                                data['data']['x'],
                                data['data']['y'],
                                data['data']['z'],
                                data['data']['roll'],
                                data['data']['pitch'],
                                data['data']['yaw']))
            print("run end")
        if data['cmd'] == "target":
            rospy.loginfo("TARGET!!!")
            msg = PoseStamped()
            msg.header.frame_id = 'base_link'
            msg.pose.position.x = data['data']["position"]["x"]
            msg.pose.position.y = data['data']["position"]["y"]
            msg.pose.position.y = data['data']["position"]["y"]
            msg.pose.orientation.x = data['data']["orientation"]["x"]
            msg.pose.orientation.y = data['data']["orientation"]["y"]
            msg.pose.orientation.z = data['data']["orientation"]["z"]
            msg.pose.orientation.w = 1
            while self.publisher.get_num_connections()<1:
                print("not yet")
                pass
            self.publisher.publish(msg)
            print("target end")
        if data['cmd'] == "stop":
            rospy.loginfo("STOP!!!")
            os.system("nohup rosnode kill trace_generator >> /home/autoware/kill.log 2>&1 &")
            os.system("nohup rosnode kill carla_ros_bridge >> /home/autoware/kill.log 2>&1 &")
            os.system("nohup rosnode kill vision_darknet_detect >> /home/autoware/kill.log 2>&1 &")
            print("stop end")
    
    
    def listener(self):
        rospy.init_node('local_controller', anonymous=False, disable_signals=False)

        rospy.Subscriber("ros_manager", String, self.callback)

        rospy.spin()

if __name__ == '__main__':
    local_controller = LocalController()
    local_controller.listener()