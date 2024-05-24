# Autoware in CARLA

The carla autoware bridge is now hosted and maintained [here](https://github.com/Autoware-AI/simulation/tree/master/carla_simulator_bridge).

This repository contains a demonstrator of an autoware agent ready to be executed with CARLA.

**The carla autoware integration requires CARLA 0.9.10.1. You can download it from [here](https://github.com/carla-simulator/carla/releases/tag/0.9.10.1)**

## CARLA autoware agent
The autoware agent is provided as a ROS package. All the configuration can be found inside the `carla-autoware-agent` folder.

![carla-autoware](docs/images/carla_autoware.png)

The easiest way to run the agent is by building and running the provided docker image.

### Requirements

- Docker (19.03+)
- Nvidia docker (https://github.com/NVIDIA/nvidia-docker)

### Setup

Firstly clone the carla autoware repository, where additional [autoware contents](https://bitbucket.org/carla-simulator/autoware-contents.git) are included as a submodule:

Afterwards, build the image with the following command:

```sh
cd carla-autoware && ./build.sh
```

This will generate a `carla-autoware:latest` docker image.

### Run the agent

1. Run a CARLA server.

```
./CarlaUE4.sh
```

2. Build carla-autoware-sdg image

```sh
docker build -t carla-autoware-sdg -f Dockerfile_sdg .
```

3. Run

```sh
./run_sdg.sh
```

## CARLA Autoware contents
The [autoware-contents](https://bitbucket.org/carla-simulator/autoware-contents.git) repository contains additional data required to run Autoware with CARLA, including the point cloud maps, vector maps and configuration files.

## Debug

在local_controller目录下有`send_message.py`，可以对`local_controller_ws_server.py`发送命令，用于调试。

本地运行需要安装Python依赖websockets。启动send_message

```
python ros_manager_debug.py
```

可以输入任意命令，观察local_controller_ws_server是否收到。

特殊命令：

- `run`: local_controller_ws_server会开启autoware和trace_generator
- `target`: local_controller_ws_server会发送目标坐标
- `stop`: local_controller_ws_server会停止autoware和trace_generator
- `exit`: 退出ros_manager_debug

## Rviz
If you don't want to use Rviz which will run by default, open file `/home/autoware/carla-autoware/carla-autoware-agent/launch/carla_autoware_agent.launch` within the container and comment line 74-75. After that the end of the file shall look like

```
  ......(previous content)
  <!--
    ###################
    ## Visualization ## 
    ###################
  -->
  <!-- <arg name='rvizconfig' default='$(find carla_autoware_agent)/$(arg agent)/rviz/config.rviz'/>
  <node name='rviz' pkg='rviz' type='rviz' args='-d $(arg rvizconfig)'/> -->

</launch>
```