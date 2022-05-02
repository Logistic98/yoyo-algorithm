# 基于python3.7镜像创建新镜像
FROM python:3.7
# 创建容器内部目录
RUN mkdir /code
# 将项目复制到内部目录
ADD src /code/
# 切换到工作目录
WORKDIR /code
# 安装项目依赖
RUN apt update
RUN apt install libgl1-mesa-glx -y
RUN pip install paddlepaddle==2.2.0 -i https://mirror.baidu.com/pypi/simple
RUN pip install "paddleocr>=2.0.1"
RUN pip install paddlenlp==2.2.4
RUN pip install -r requirements.txt
# 放行端口
EXPOSE 5001
# 启动项目
ENTRYPOINT ["nohup","python","server.py","&"]