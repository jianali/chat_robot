FROM python:3.7
# /app 是父目录，可以改成产品名称

COPY . /app
# 可以把log 挂载出来，统一格式
VOLUME /var/transwarp
WORKDIR /app
RUN pip install -r requirements.txt -i https://pypi.doubanio.com/simple
EXPOSE 8001 8001
# python -m sanic chat_server.app --host=0.0.0.0 --port=1337 --workers=4
ENTRYPOINT ["python", "/app/chat_server.py"]