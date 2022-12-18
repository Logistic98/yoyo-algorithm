# 基于python3.7镜像创建新镜像
FROM python:3.7
# 创建容器内部目录
RUN mkdir /code
# 将项目复制到内部目录
ADD . /code/
# 切换到工作目录
WORKDIR /code
# 安装项目依赖
RUN pip install -r requirements.txt
RUN pip install https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-2.6.0-cp37-cp37m-manylinux2010_x86_64.whl
RUN apt update && apt install libgl1-mesa-glx -y
# 放行端口
EXPOSE 5004
# 启动项目
ENTRYPOINT ["nohup","python","server.py","&"]