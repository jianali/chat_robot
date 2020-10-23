import sanic
import httpx
from sanic import Sanic
from sanic.response import json
from sanic.websocket import WebSocketProtocol
from sanic.exceptions import NotFound
from sanic.response import html
from sanic.response import text
import json
import re

# 解决跨域访问的问题
from sanic_cors import CORS
from jinja2 import Environment, PackageLoader

from app.service.DiagnosticTree import DiagnosticTree
from app.model.GuideTreeInfo import GuideTreeInfo
from app.service.NoticeService import NoticeService
from app.service.RobotService import RobotService
from app.service.GuideTreeService import GuideTreeService
from app.util.CommonUtil import CommonUtil
from app.util.OrmUtil import OrmUtil
from app.util.DateEncoder import DateEncoder

from app.util.MysqlUtil import MysqlUtil,Pmysql

env = Environment(loader=PackageLoader('app', 'templates'))
app = Sanic(__name__)
CORS(app)
# loop = asyncio.get_event_loop()
# pool = await Pmysql.create_pool(loop, user='root', password='', db='aiops')

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

# 测试返回根节点信息
@app.route('/getrootnode')
async def getGuideNode(request):
    args = request.get_args(keep_blank_values=True)
    id=args.get('id')
    guideNodeResult=await GuideTreeService().getRootNode(id)
    return text(json.dumps({'resultdesc': 'Notice相关信息如下：', 'resultdata': guideNodeResult}, cls = DateEncoder))

# 测试返回节点信息
@app.route('/getnodeinfo')
async def getGuideNode(request):
    args = request.get_args(keep_blank_values=True)
    id=args.get('id')
    guideNodeResult=await GuideTreeService().getNode(id)
    return text(json.dumps({'resultdesc': 'nodeinfo', 'resultdata':guideNodeResult},cls=DateEncoder))


# 测试返回节点信息
@app.route('/deletenode')
async def getGuideNode(request):
    args = request.get_args(keep_blank_values=True)
    id = args.get('id')
    guideNodeResult = await GuideTreeService().deleteNode(id)
    return text(json.dumps({'resultdesc': '删除节点状态：', 'resultdata':guideNodeResult}))


                           # 测试修改节点信息
@app.route('/modifynodeinfo',methods=['POST'])
async def modifyGuideNode(request):
    args = request.json
    guideNodeResult = await GuideTreeService().modifyNode(args)
    return text(json.dumps({'resultdesc':'修改节点状态：', 'resultdata':guideNodeResult}))

# 新增引导节点
@app.route('/insertsubnode',methods=['POST'])
async def insertSubNode(request):
    args = request.json
    guideNodeResult = await GuideTreeService().insertNode(args)
    return text(json.dumps({'resultdesc':'新增节点状态','resultdata':guideNodeResult}))


# 测试返回节点树状结构信息
@app.route('/nodetree')
async def getGuideTree(request):
    args = request.get_args(keep_blank_values=True)
    id = args.get('id')
    guideTreeResult = await GuideTreeService().getGuideTrees(id)
    return text(guideTreeResult)

# 测试返回备选的文章列表
@app.route('/getarticlelist')
async def getArticlelist(request):
    args = request.get_args(keep_blank_values=True)
    title = args.get('title')
    components=args.get('components')
    product_type=args.get('product_type')
    articleListResult = await GuideTreeService().getArticleList(title,components,product_type)
    return text(json.dumps({'resultdesc': '文章列表：', 'resultdata':articleListResult}))

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
        # # 如果无法识别走第三方接口开始尬聊
        # intelligence_data = {"key": "free", "appid": 0, "msg": user_msg}
        # r = httpx.get("http://api.qingyunke.com/api.php", params=intelligence_data)
        # chat_msg = r.json()["content"]
        # print('Sending: ' + chat_msg)
        # await ws.send(chat_msg)
        # 根据发送过来的消息进行区分，访问数据库中的导引信息推送给客户端
        if (user_msg.replace("\n", "").strip()=='引导'):
            guideResult=await RobotService().guideMessage(0)
            # 这里手动封装一个orm，dto中定义数据模型
            await ws.send(guideResult)

        elif(user_msg.find('引导')==0 and CommonUtil.is_number(re.findall("\d+",user_msg)[0])):
            guideResult = await RobotService().guideMessage(int(re.findall("\d+",user_msg)[0]))
            await ws.send(guideResult)
        else:
            # 如果识别不了，可以默认推送相关引导提示消息
            await ws.send(json.dumps({'resultdesc': "<br>"+RobotService().defaultChatMessage(), 'resultdata':''}))


# 测试返回解析好的html文件
#         a = DiagnosticNode(1, None, '根节点', [])
#         a.setChidNodes(DiagnosticNode(3, 1, '第一层目录', []))
#         a.setChidNodes(DiagnosticNode(4, 1, '第一层目录', []).setChidNodes(DiagnosticNode(5, 4, '第二层目录', [])))

# 开始测试
#         await ws.send(DiagnosticTree.toHtml(a))


# --------------------------



if __name__ == "__main__":
    app.error_handler.add(
        NotFound,
        lambda r, e: sanic.response.empty(status=404)
    )

    app.run(host="0.0.0.0", port=8001, protocol=WebSocketProtocol, debug=True ,workers=4)

