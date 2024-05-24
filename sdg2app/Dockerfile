# If you want to use the original image from Docker Hub, use the tiangolo one
# FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
FROM registry.cn-beijing.aliyuncs.com/selfdriveguard/uvicorn-gunicorn-fastapi:python3.8

COPY ./requirements.txt /requirements.txt

# If you don't need to use the tuna mirror, comment first two lines below 
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install -r /requirements.txt

COPY ./src/sdgApp /app