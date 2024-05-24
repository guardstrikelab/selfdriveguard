# coding=UTF-8

import docker
import os
from os.path import abspath, join, dirname


def main():
    run()


def run():
    client = docker.from_env()

    ROOT_PATH = abspath(dirname(__file__))
    CONTENTS_PATH = join(ROOT_PATH, "autoware-contents")
    SCRIPTS_PATH = join(ROOT_PATH, "scripts")

    ros_container = client.containers.run("registry.cn-beijing.aliyuncs.com/ad-test/carla-autoware-extern:1.0.1",
                                          detach=True,
                                          volumes={CONTENTS_PATH: {'bind': '/home/autoware/autoware-contents', 'mode': 'ro'},
                                                   SCRIPTS_PATH: {'bind': '/home/autoware/my_scripts', 'mode': 'ro'}},
                                          runtime='nvidia',
                                          network='host',
                                          privileged=True,
                                          environment=["DISPLAY={}".format(
                                              os.getenv('DISPLAY'))],
                                          tty=True
                                          )

    # ros_container = client.containers.run("registry.cn-beijing.aliyuncs.com/ad-test/carla-autoware-extern:1.0.1",
    #                                       detach=True,
    #                                       volumes={CONTENTS_PATH: {'bind': '/home/autoware/autoware-contents', 'mode': 'ro'},
    #                                                SCRIPTS_PATH: {'bind': '/home/autoware/my_scripts', 'mode': 'ro'}},
    #                                       runtime='nvidia',
    #                                       network='host',
    #                                       privileged=True,
    #                                       environment=["DISPLAY={}".format(
    #                                           os.getenv('DISPLAY'))],
    #                                       tty=True,
    #                                       user="autoware",
    #                                       command="/bin/bash -i -c 'roslaunch rosbridge_server rosbridge_websocket.launch'"
    #                                       )

    print("Container id:{}".format(ros_container.short_id))
    print("Command to enter container:\n docker exec -it --user autoware {} bash".format(ros_container.short_id))


if __name__ == '__main__':
    main()
