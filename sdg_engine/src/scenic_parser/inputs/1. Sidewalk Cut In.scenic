""" Scenario Description
37 pre-crash
17. Vehicle(s) Parking – Vehicles Traveling in Same Direction
Voyage OAS Scenario Unique ID: 2-2-XX-CF-STR-CAR:Pa>E:03
The car ahead of ego that is badly parked over the sidewalk cuts into ego vehicle's lane.
This scenario may fail if there exists any obstacle (e.g. fences) on the sidewalk 
"""

## SET MAP AND MODEL (i.e. definitions of all referenceable vehicle types, road library, etc)
param map = localPath('../third-party/scenic/CARLA/Town01.xodr')  # or other CARLA map that definitely works
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
SAFETY_DISTANCE = 8
PARKING_SIDEWALK_OFFSET_RANGE = 2
CUT_IN_TRIGGER_DISTANCE = Range(20, 30)
EGO_SPEED = 8
PARKEDCAR_SPEED = 40

## DEFINING BEHAVIORS
behavior CutInBehavior(laneToFollow, target_speed):
	while (distance from self to ego) > CUT_IN_TRIGGER_DISTANCE:
		wait

	do FollowLaneBehavior(laneToFollow = laneToFollow, target_speed=target_speed)

behavior CollisionAvoidance():
	while withinDistanceToAnyObjs(self, SAFETY_DISTANCE):
		take SetBrakeAction(MAX_BREAK_THRESHOLD)


behavior EgoBehavior(target_speed):
	try: 
		do FollowLaneBehavior(target_speed=target_speed)

	interrupt when withinDistanceToAnyObjs(self, SAFETY_DISTANCE):
		do CollisionAvoidance()

## DEFINING SPATIAL RELATIONS
# Please refer to scenic/domains/driving/roads.py how to access detailed road infrastructure
# 'network' is the 'class Network' object in roads.py
roads = network.roads

# make sure to put '*' to uniformly randomly select from all elements of the list of roads
select_road = network.roads[0]

# in roads.py, the 'class Road' contains 'lanes' which is a list of lanes whose rightmost lane is indexed 0
ego_lane = select_road.lanes[0]

ego = Car at 370 @ 0,
		with behavior EgoBehavior(target_speed=EGO_SPEED),
		with rolename "AV_EGO"

spot = OrientedPoint on visible curb
parkedHeadingAngle = Uniform(1,0)*Range(10,20) deg

other = Car left of (spot offset by PARKING_SIDEWALK_OFFSET_RANGE @ 0), facing parkedHeadingAngle relative to ego.heading,
			with behavior CutInBehavior(ego_lane, target_speed=PARKEDCAR_SPEED),
			with regionContainedIn None

require (angle from ego to other) - ego.heading < 0 deg
require 10 < (distance from ego to other) < 15