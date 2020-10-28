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
        return str("欢迎您的访问~我是阿环！<b>请选择出问题的组件</b>，再根据引导<b>输入编号</b>一步步解决问题呦！"
                   "<br>"
                   "选择组件之后，对应组件的Notice和工具也在右边呦，自助食用~~~→_→")


    #用于返回告示中的notice邮件，可以将notice邮件做一个组件分类



    #用于引导的信息
    async def guideMessage(self,id):
        guideResult =  await GuideTreeService().getRootNode(id)
        if str(id)!='0':
            guideNodeResult = await GuideTreeService().getNode(id)
        else:
            guideNodeResult = '请选择如下编号：'
        # 这里手动封装一个orm，dto中定义数据模型
        result=json.dumps({'resultdesc': guideNodeResult, 'resultdata': guideResult},
                           cls=DateEncoder)
        return result

if __name__ == '__main__':
    a=RobotService().defaultChatMessage()
    print(str(a))