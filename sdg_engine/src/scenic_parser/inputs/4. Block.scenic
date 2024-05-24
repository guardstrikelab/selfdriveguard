""" Scenario Description
37 pre-crach
36. Vehicle Contacting Object without Prior Vehicle Maneuver
Control loss without previous action.
The ego-vehicle loses control due to bad conditions on the road and it must recover, coming back to
its original lane.
"""

## SET MAP AND MODEL (i.e. definitions of all referenceable vehicle types, road library, etc)
param map = localPath('../third-party/scenic/CARLA/Town01.xodr')  # or other CARLA map that definitely works
param carla_map = 'Town01'
param weather = 'MidRainSunset'
model scenic.simulators.carla.model

## CONSTANTS
EGO_MODEL = "vehicle.lincoln.mkz2017"
EGO_SPEED = 10

## DEFINING BEHAVIORS
# EGO BEHAVIOR: Follow lane, and brake after passing a threshold distance to the leading car
behavior EgoBehavior(speed=10):
    do FollowLaneBehavior(speed)

## DEFINING SPATIAL RELATIONS
# Please refer to scenic/domains/driving/roads.py how to access detailed road infrastructure
# 'network' is the 'class Network' object in roads.py

# make sure to put '*' to uniformly randomly select from all elements of the list, 'lanes'
lane = Uniform(*network.lanes)

start = OrientedPoint on lane.centerline
ego = Car at start,
    with rolename "AV_EGO",
    with blueprint EGO_MODEL,
    with behavior EgoBehavior(EGO_SPEED)

debris1 = Debris ahead of start by Range(10, 20)
debris2 = VendingMachine following roadDirection from debris1 for Range(5, 10)
debris3 = Debris following roadDirection from debris2 for Range(5, 10)
debris4 = Debris right of debris1 by Range(1, 3)
debris5 = Trash following roadDirection from debris4 for Range(5, 10)
debris6 = Bench following roadDirection from debris5 for Range(5, 10)
debris7 = Debris left of debris1 by Range(2, 4)
debris8 = Bench following roadDirection from debris7 for Range(5, 10)