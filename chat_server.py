import sanic
import httpx
from sanic import Sanic
from sanic.response import json
from sanic.websocket import WebSocketProtocol
from sanic.exceptions import NotFound
from sanic.response import html
from sanic.response import text
import json

# 解决跨域访问的问题
from sanic_cors import CORS


from jinja2 import Environment, PackageLoader

from app.service.DiagnosticTree import DiagnosticTree
from app.model.DiagnosticNode import DiagnosticNode
from app.service.NoticeService import NoticeService
from app.service.GuideTreeService import GuideTreeService
from app.util.CommonUtil import CommonUtil
from app.util.OrmUtil import OrmUtil
from app.util.DateEncoder import DateEncoder

env = Environment(loader=PackageLoader('app', 'templates'))

app = Sanic(__name__)

CORS(app)

@app.route('/')
async def index(request):
    """
    聊天页面
    """
    template = env.get_template('index.html')
    html_content = template.render(title='聊天机器人')
    return html(html_content)


# 测试heros
@app.route('/heros')
async def getHeros(request):
    return text(json.dumps('[{"id":1,"name":"ironMan"},{"id":2,"name":"lijian"},{"id":3,"name":"miaomiao"},{"id":4,"name":"jack"}]'))

# 测试notice
@app.route('/notice')
async def getComponentNotice(request):
    args = request.get_args(keep_blank_values=True)
    component=args.get('component')
    noticeResult=await NoticeService().componentNoticeMessage(component)
    return text(json.dumps({'resultdesc': 'Notice相关信息如下：', 'resultdata': OrmUtil.toMap(noticeResult,
                                                                                            ["id", "description",
                                                                                             "solution", "esid",
                                                                                             "subassembly_name", "moudle","last_modified_date"])},cls=DateEncoder))




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


# -----------------------------
        # 根据发送过来的消息进行区分，访问数据库中的导引信息推送给客户端
        if (user_msg.find('引导')==0):
            guideResult=await GuideTreeService().getGuideTree(0)
            print(guideResult)
            # 这里手动封装一个orm，dto中定义数据模型
            await ws.send(json.dumps({'resultdesc': '请选择如下编号：', 'resultdata': OrmUtil.toMap(guideResult,
                                                                                            ["id", "parent_id",
                                                                                             "guide_name", "level",
                                                                                             "article_id", "author",
                                                                                             "publish_date",
                                                                                             "modify_date"])},
                                     cls=DateEncoder))
        elif(CommonUtil.is_number(user_msg)):
            guideResult = await GuideTreeService().getGuideTree(int(user_msg))
            await ws.send(json.dumps({'resultdesc': '请选择如下编号：', 'resultdata': OrmUtil.toMap(guideResult,
                                                                                            ["id", "parent_id",
                                                                                             "guide_name", "level",
                                                                                             "article_id", "author",
                                                                                             "publish_date",
                                                                                             "modify_date"])},
                                     cls=DateEncoder))
        else:
            # 如果识别不了，可以默认推送相关引导提示消息
            await ws.send(json.dumps({'resultdesc': NoticeService().defaultChatMessage(), 'resultdata':''}))


# 测试返回解析好的html文件
#         a = DiagnosticNode(1, None, '根节点', [])
#         a.setChidNodes(DiagnosticNode(3, 1, '第一层目录', []))
#         a.setChidNodes(DiagnosticNode(4, 1, '第一层目录', []).setChidNodes(DiagnosticNode(5, 4, '第二层目录', [])))

# 开始测试
#         await ws.send(DiagnosticTree.toHtml(a))


# --------------------------
        # # 如果无法识别走第三方接口开始尬聊
        # intelligence_data = {"key": "free", "appid": 0, "msg": user_msg}
        # r = httpx.get("http://api.qingyunke.com/api.php", params=intelligence_data)
        # chat_msg = r.json()["content"]
        # print('Sending: ' + chat_msg)
        # await ws.send(chat_msg)


if __name__ == "__main__":
    app.error_handler.add(
        NotFound,
        lambda r, e: sanic.response.empty(status=404)
    )
    app.run(host="0.0.0.0", port=8001, protocol=WebSocketProtocol, debug=True)

