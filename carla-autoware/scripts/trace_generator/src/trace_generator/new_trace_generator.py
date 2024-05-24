#!/usr/bin/python
import roslibpy
import time
import json
import message_filters
import math
import os
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import TwistStamped
from autoware_msgs.msg import DetectedObjectArray
from derived_object_msgs.msg import ObjectArray
from carla_msgs.msg import CarlaEgoVehicleStatus
from grid_map_msgs.msg import GridMap
from trace import *

TIME = time.time()
f = open(os.environ['HOME']+"/out.txt","w")
"""

[geometry_msgs/PoseStamped]:
std_msgs/Header header
  uint32 seq
  time stamp
  string frame_id
geometry_msgs/Pose pose
  geometry_msgs/Point position
    float64 x
    float64 y
    float64 z
  geometry_msgs/Quaternion orientation
    float64 x
    float64 y
    float64 z
    float64 w


[geometry_msgs/TwistStamped]:
std_msgs/Header header
  uint32 seq
  time stamp
  string frame_id
geometry_msgs/Twist twist
  geometry_msgs/Vector3 linear
    float64 x
    float64 y
    float64 z
  geometry_msgs/Vector3 angular
    float64 x
    float64 y
    float64 z

"""

def distance(posA, posB):
	return math.sqrt((posA.x-posB.x)*(posA.x-posB.x) + (posA.y-posB.y)*(posA.y-posB.y))


def callback(pose_msg, velocity_msg, accel_msg, ground_truths_msg, perceptions_msg):
	print("Callback called")
	global TIME
	if(time.time() - TIME < 1):
		return
	TIME = time.time()
	trace = {}
	ground_truths_in_range = []
	perceptions = []

	for obj in ground_truths_msg.objects:
		ground_truth = GroundTruth(pose_msg, obj)
		ground_truths_in_range.append(ground_truth.data())

	for obj in perceptions_msg.objects:
		perception = Perception(obj)
		perceptions.append(perception.data())
		
	ego = Ego(pose_msg, velocity_msg, accel_msg)
	
	trace['time'] = pose_msg.header.stamp
	trace["ego"] = ego.data()
	trace["perceptions"] = perceptions
	trace["ground_truths"] = ground_truths_in_range

	print(str(trace))

	f.write(str(trace)+"\n")



def listen():
    client = roslibpy.Ros(host='localhost', port=9090)
    client.run()
    listener = roslibpy.Topic(client, '/trace_generator', 'std_msgs/String')
    listener.subscribe(lambda message: print('Heard talking: ' + message['data']))
	pose = message_filters.Subscriber("/current_pose", PoseStamped)	
	velocity = message_filters.Subscriber("/current_velocity", TwistStamped)	
	accel = message_filters.Subscriber("/carla/ego_vehicle/vehicle_status", CarlaEgoVehicleStatus)
	ground_truth = message_filters.Subscriber("/carla/ego_vehicle/objects", ObjectArray)
	perception = message_filters.Subscriber("/prediction/motion_predictor/objects", DetectedObjectArray)
	#grid_map = message_filters.Subscriber("/grid_map_wayarea", GridMap.info)
	#perception = message_filters.Subscriber("/ground_truth/objects", DetectedObjectArray)
	#/detection/lidar_tracker/objects /prediction/motion_predictor/objects

	ts = message_filters.TimeSynchronizer([pose,velocity,accel, ground_truth, perception], 10)
	ts.registerCallback(callback)
	rospy.spin()


if __name__ == '__main__':
     listen()
