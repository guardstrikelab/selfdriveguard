# SDG-Engine



## Getting Started from Source



#### Prerequisites

- ubuntu 18.04

- python == 3.8

- pip

- poetry 

  > Poetry is a tool for **dependency management** and **packaging** in Python. See more detailed information at https://python-poetry.org/
  >
  > python 3.8 with pip and poetry can be downloaded by:
  >
  > ```bash
  > sudo apt-get update
  > sudo apt-get install python3.8
  > sudo apt-get install python3-pip
  > pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U
  > pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
  > pip install poetry
  > ```

- Other system dependencies

  ```bash
  sudo apt-get install libxerces-c3.2 libjpeg8 libtiff5 iputils-ping
  ```

  

#### How to run



1. Installation

   ```bash
   # download repo
   git clone https://codeup.aliyun.com/5f3f374f6207a1a8b17f933f/SelfDriveGuard/SelfDriveGuard_New/sdg_engine_lite_version.git
   
   # go to the folder where the pyproject.toml is
   poetry export -f requirements.txt --output requirements.txt --without-hashes
   pip install -r requirements.txt
   ```

2. Run carla-autoware

   ```bash
   # step 1
   docker pull registry.cn-beijing.aliyuncs.com/ad-test/carla-autoware-extern:2.0.0
   ```

   ```bash
   # step 2
   git clone git@codeup.aliyun.com:5f3f374f6207a1a8b17f933f/SelfDriveGuard/carla-autoware.git
   cd carla-autoware
   unzip autoware-contents.zip
   rm autoware-contents.zip
   ```

   ```bash
   # step 3
   # create this yaml file outside carla-autoware folder: 
   ```

   ```yaml
   services:
       autoware:
               image: registry.cn-beijing.aliyuncs.com/ad-test/carla-autoware-extern:2.0.0
               volumes: 
                   - ./carla-autoware/autoware-contents:/home/autoware/autoware-contents:ro
                   - ./carla-autoware/scripts:/home/autoware/my_scripts:ro
               environment: 
                   NVIDIA_VISIBLE_DEVICES: all
                   CARLA_SERVER_IP: "simulator"
               ports: 
                   - "9090:9090"
                   - "9091:9091"
               runtime: nvidia
   ```

   ```bash
   # step 4
   docker-compose -f docker-compose.yml -p autoware up
   ```

   

2. Configuration

   ```python
   # sdg_engine_lite_version/src/main/engine 找到以下环境变量进行配置：
   
   
   CARLA_SERVER_IP  # carla server
   
   ROS_BRIDGE_IP   # carla-autoware 
   
   # sdg_engine_lite_version/src/test_engine 找到content.ini文件进行变量配置
   host # 本机IP 
   port # default 8093
   ```
   
3. Run

   ```bash
   cd ./
   python main.py
   ```

  

4. Test

   ```bash
   cd ./src/test_engine
   python listen_engine_websocket.py
   ```

   
