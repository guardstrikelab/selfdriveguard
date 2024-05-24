""" Scenario Description
37 pre-crach
24/25/27. Following Vehicle Approaching a Decelerating Lead Vehicle
Voyage OAS Scenario Unique ID: 2-2-XX-CF-STR-CAR:Pa>E:03
The lead car suddenly stops and then resumes moving forward
"""

## SET MAP AND MODEL (i.e. definitions of all referenceable vehicle types, road library, etc)
param map = localPath('../third-party/scenic/CARLA/Town01.xodr')  
param carla_map = 'Town01'
param weather = {
  'cloudiness': 0,
  'precipitation': 0,
  'precipitation_deposits': 0,
  'sun_azimuth_angle': 0,
  'sun_altitude_angle': 90
}
model scenic.simulators.carla.model #located in scenic/simulators/carla/model.scenic

## CONSTANTS
MAX_BREAK_THRESHOLD = 1
SAFETY_DISTANCE = 10
INITIAL_DISTANCE_APART = -16
STEPS_PER_SEC = 10

## DEFINING BEHAVIORS
behavior LeadCarBehavior():
	try:
		do FollowLaneBehavior()
	interrupt when 30 < simulation().currentTime and 30 < simulation().currentTime % 100 and simulation().currentTime % STEPS_PER_SEC < 90:
		take SetBrakeAction(MAX_BREAK_THRESHOLD)

behavior CollisionAvoidance():
	while withinDistanceToAnyObjs(self, SAFETY_DISTANCE):
		take SetBrakeAction(MAX_BREAK_THRESHOLD)

behavior FollowLeadCarBehavior():
	try: 
		do FollowLaneBehavior()

	interrupt when withinDistanceToAnyObjs(self, SAFETY_DISTANCE):
		do CollisionAvoidance()

## DEFINING SPATIAL RELATIONS
# Please refer to scenic/domains/driving/roads.py how to access detailed road infrastructure
# 'network' is the 'class Network' object in roads.py
roads = network.roads

# make sure to put '*' to uniformly randomly select from all elements of the list
select_road = Uniform(*roads)
select_lane = Uniform(*select_road.lanes)

## OBJECT PLACEMENT
other = Car at 370 @ 2,
		with behavior LeadCarBehavior()

ego = Car following roadDirection from other for INITIAL_DISTANCE_APART,
		with rolename "AV_EGO",  	
		with behavior FollowLeadCarBehavior()