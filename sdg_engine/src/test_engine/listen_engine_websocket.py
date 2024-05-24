import asyncio
from conf_parse import get_conf
import websockets
# import redisUtil
import json
import time
import sys, os
import time
# from mongoUtil import mongoDB_repo
# from mongoSession import mongo_session
import socket

sys.path.append('../')


async def send_cmd_code(websocket, cmd, code, timeLimit):
    request = {
        'cmd': cmd,
        'code': code,
        'time': timeLimit
    }

    await websocket.send(json.dumps(request))


# async def send_cmd(websocket, cmd):
#     request = {
#         'cmd': cmd,
#     }
#     await websocket.send(json.dumps(request))


async def recv_result(websocket):
    while True:
        # await send_cmd(websocket,"stop")

        recv_text = await websocket.recv()
        recv = json.loads(recv_text)
        print(recv)

        # if "state" in recv:
        #     mongoDB_repo(mongo_session()).update_status(taskId, recv["state"])
        #
        # if 'cmd' in recv:
        #     if recv['cmd'] == "CRITERIA":
        #         mongoDB_repo(mongo_session()).update_result(taskId, recv['msg'])
        #         # await redisUtil.RedisTT().deleteTask(taskId) #执行结束之后删除redis中缓存的task
        #     if recv['cmd'] == "STOP":
        #         break
        # time.sleep(1)

with open("input.txt", 'r') as f:
    scenest_content = f.read()


# 客户端主逻辑
async def main_logic(conf, url):
    async with websockets.connect(url) as websocket:
        # taskid = conf['CONTENT']['taskid']
        code = scenest_content
        timeLimit = int(conf['CONTENT']['timeLimit'])
        cmd = "run"
        await send_cmd_code(websocket, cmd, code, timeLimit)
        # taskId = bytes.decode(taskid)
        await recv_result(websocket)
        await websocket.close()


if __name__ == "__main__":
    conf = get_conf()

    host = os.environ.get('Websocket_host')
    if host is None:
        host = str(conf['CONTENT']['host'])

    port = os.environ.get('Websocket_port')
    if port is None:
        port = str(conf['CONTENT']['port'])

    url = "ws://" + host + ":" + port
    userId = str(os.environ.get('UserId'))
    if userId is None:
        userId = str(conf['CONTENT']['user_id'])

    while True:
        # taskList = redisUtil.RedisTT().r.lrange(userId, 0, -1)
        # if len(taskList) <= 0:
        print("请添加任务")
        # time.sleep(5)
        # else:
        asyncio.get_event_loop().run_until_complete(main_logic(conf, url))
