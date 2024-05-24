#!/usr/bin/python
import rospy
import time
import message_filters
import json
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import TwistStamped
from autoware_msgs.msg import DetectedObjectArray
from derived_object_msgs.msg import ObjectArray
from carla_msgs.msg import CarlaEgoVehicleStatus
from grid_map_msgs.msg import GridMap
from trace import Ego, GroundTruth, Perception
from std_msgs.msg import String

class TraceGenerator():
	def __init__(self):
		self.TIME = time.time()
		# self.file = open(os.environ['HOME']+"/out.txt","w")
		self.publisher = rospy.Publisher('trace', String, queue_size=100)


	# def distance(posA, posB):
	# 	return math.sqrt((posA.x-posB.x)*(posA.x-posB.x) + (posA.y-posB.y)*(posA.y-posB.y))


	def callback(self, pose_msg, velocity_msg, accel_msg, ground_truths_msg, perceptions_msg):
		# global TIME
		if(time.time() - self.TIME < 1):
			return
		self.TIME = time.time()
		ground_truths_in_range = {}
		perceptions = {}

		for obj in ground_truths_msg.objects:
			ground_truth = GroundTruth(pose_msg, obj)
			ground_truths_in_range[str(ground_truth.tag)] = ground_truth.data()
		# TODO: use real traffic
		ground_truths_in_range['traffic'] = (100,200)
		

		for obj in perceptions_msg.objects:
			perception = Perception(obj)
			perceptions[str(perception.tag)] = perception.data()
		perceptions['traffic'] = (100, 200)
			
		ego = Ego(pose_msg, velocity_msg, accel_msg)

		data = json.dumps({
            "time": str(pose_msg.header.stamp),
			"ego":ego.data(),
			"perception": perceptions,
			"truth": ground_truths_in_range
        })


		print(data)
		self.publisher.publish(str(data))

		# f.write(str(trace)+"\n")



	def listen(self):
		rospy.init_node('trace_generator', anonymous=False)
		pose = message_filters.Subscriber("/current_pose", PoseStamped)	
		velocity = message_filters.Subscriber("/current_velocity", TwistStamped)	
		accel = message_filters.Subscriber("/carla/ego_vehicle/vehicle_status", CarlaEgoVehicleStatus)
		ground_truth = message_filters.Subscriber("/carla/ego_vehicle/objects", ObjectArray)
		perception = message_filters.Subscriber("/prediction/motion_predictor/objects", DetectedObjectArray)
		#grid_map = message_filters.Subscriber("/grid_map_wayarea", GridMap.info)
		#perception = message_filters.Subscriber("/ground_truth/objects", DetectedObjectArray)
		#/detection/lidar_tracker/objects /prediction/motion_predictor/objects

		ts = message_filters.TimeSynchronizer([pose,velocity,accel, ground_truth, perception], 10)
		ts.registerCallback(self.callback)
		rospy.spin()


if __name__ == '__main__':
	trace_generator = TraceGenerator()
	trace_generator.listen()
