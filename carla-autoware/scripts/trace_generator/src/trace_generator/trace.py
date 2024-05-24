# from geometry_msgs.msg import PoseStamped
# from geometry_msgs.msg import TwistStamped
# from autoware_msgs.msg import DetectedObjectArray
# from derived_object_msgs.msg import ObjectArray
# from carla_msgs.msg import CarlaEgoVehicleStatus
# from grid_map_msgs.msg import GridMap

PERCISION = 4

"""
Ego:
	pos: 		(x, y),
	heading: 	(x, y ,z, w),
	velocity:	(x, y),
	accel:		(x, y)


GroundTruth:
	tag:		string,
	pos:		(x, y),
	heading:	(x, y, x, w),
	velocity:	(x, y),
	size:		(x, y ,z)


Perception:
	pos:		(x, y),
	heading:	(x, y, x, w),
	velocity:	(x, y),
	size:		(x, y ,z)
"""
class Ego:
	def __init__(self, pose_msg, velocity_msg, accel_msg):
		self.pos = (pose_msg.pose.position.x, pose_msg.pose.position.y)
		self.heading = (pose_msg.pose.orientation.x, pose_msg.pose.orientation.y, pose_msg.pose.orientation.z, pose_msg.pose.orientation.w)
		self.velocity=(velocity_msg.twist.linear.x, velocity_msg.twist.linear.y)
		self.accel=(accel_msg.acceleration.linear.x, accel_msg.acceleration.linear.y)

	def data(self):
		return (self.pos, self.heading, self.velocity, self.accel)

class GroundTruth:
	# pose_msg indicates position of the ego vehicle
	def __init__(self, pose_msg, obj_msg):
		obj_msg.pose.position.x -= pose_msg.pose.position.x 
		obj_msg.pose.position.y -= pose_msg.pose.position.y
		self.tag = ""
		if(obj_msg.classification == 4):
			self.tag = "pedestrian_"
		elif(obj_msg.classification >= 5 and obj_msg.classification <= 9):
			self.tag = "npc_"
		self.tag += str(obj_msg.id)
		self.pos = (obj_msg.pose.position.x, obj_msg.pose.position.y)
		self.heading=(obj_msg.pose.orientation.x, obj_msg.pose.orientation.y, obj_msg.pose.orientation.z, obj_msg.pose.orientation.w)
		self.velocity=(obj_msg.twist.linear.x, obj_msg.twist.linear.y)
		self.size = (obj_msg.shape.dimensions[0], obj_msg.shape.dimensions[1], obj_msg.shape.dimensions[2])

	def data(self):	
		return (self.pos, self.heading, self.velocity, self.size)

class Perception:
	def __init__(self, obj_msg):
		self.tag = str(obj_msg.id)
		self.pos = (obj_msg.pose.position.x, obj_msg.pose.position.y)
		self.heading=(obj_msg.pose.orientation.x, obj_msg.pose.orientation.y, obj_msg.pose.orientation.z, obj_msg.pose.orientation.w)
		self.velocity=(obj_msg.velocity.linear.x, obj_msg.velocity.linear.y)
		self.size = (obj_msg.dimensions.x, obj_msg.dimensions.y, obj_msg.dimensions.z)

	def data(self):	
		return (self.pos, self.heading, self.velocity, self.size)
		
		
