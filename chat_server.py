import sanic
import httpx
from sanic import Sanic
from sanic.response import json
from sanic.websocket import WebSocketProtocol
from sanic.exceptions import NotFound
from sanic.response import html
from jinja2 import Environment, PackageLoader


env = Environment(loader=PackageLoader('app', 'templates'))

app = Sanic(__name__)


@app.route('/')
async def index(request):
    """
    聊天页面
    """
    template = env.get_template('index.html')
    html_content = template.render(title='聊天机器人')
    return html(html_content)


@app.websocket('/chat')
async def chat(request, ws):
    """
    处理聊天信息，并返回消息
    :param request:
    :param ws:
    :return:
    """
    while True:
        user_msg = await ws.recv()
        # user_msg为客户发送过来的消息
        print('Received: ' + user_msg)
        # 根据发送过来的消息进行区分，访问数据库中的导引信息推送给客户端
        if (user_msg.find("inceptor")==1) :
            await ws.send("为您找到如下排障知道，请点击链接查看。\n"
                          "1、Inceptor服务启动故障；\n"
                          "2、Inceptor性能调优及排查；\n"
                          "3、SQL编译失败；\n"
                          "4、Inceptor任务运行失败；\n")


        # 如果无法识别走第三方接口开始尬聊
        intelligence_data = {"key": "free", "appid": 0, "msg": user_msg}
        r = httpx.get("http://api.qingyunke.com/api.php", params=intelligence_data)
        chat_msg = r.json()["content"]
        print('Sending: ' + chat_msg)

        # 返回信息至聊天机器人客户端
        await ws.send(chat_msg)


if __name__ == "__main__":
    app.error_handler.add(
        NotFound,
        lambda r, e: sanic.response.empty(status=404)
    )
    app.run(host="127.0.0.1", port=8001, protocol=WebSocketProtocol, debug=True)

