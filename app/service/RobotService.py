from app.util.MysqlUtil import MysqlUtil
from app.service.GuideTreeService import GuideTreeService
from app.util.DateEncoder import DateEncoder
import json
from app.util.OrmUtil import OrmUtil
# 用于返回告示，包括重大Notice更新等相关消息

class RobotService():

    def __init__(self):
        self.__mysqlUtil=MysqlUtil()
        self.__result=""

    # 对于默认的消息，后续可以从数据库中获取（默认的notice也会实时更新）
    def defaultChatMessage(self):
        return str("欢迎您的访问~我是阿环~"
                   "小环内置多种功能，通过发送命令可执行特殊操作！！！"
                   "示例："
                   "引导：引导:{需要}"
                   "为了给您提供更准确的答复，请尽量：<br>"
                   "1、登录后再提问；<br>"
                          "2、在右侧“产品分类”中选择您要咨询的产品 ；<br>"
                   "可以尝试输入'<b>引导</b>'，让机器人为你指路呦！如您对我的答案不满意，可以立即转SLA工单处理喔！")


    #用于返回告示中的notice邮件，可以将notice邮件做一个组件分类



    #用于引导的信息
    async def guideMessage(self,id):
        guideResult =  await GuideTreeService().getRootNode(id)
        # 这里手动封装一个orm，dto中定义数据模型
        result=json.dumps({'resultdesc': '请选择如下编号：', 'resultdata': OrmUtil.toMap(guideResult,
                                                                                  ["id", "parent_id",
                                                                                   "guide_name", "level",
                                                                                   "article_id", "author",
                                                                                   "publish_date",
                                                                                   "modify_date","title"])},
                           cls=DateEncoder)
        return result

if __name__ == '__main__':
    a=RobotService().defaultChatMessage()
    print(str(a))