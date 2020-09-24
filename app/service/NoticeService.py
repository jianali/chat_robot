from app.util.MysqlUtil import MysqlUtil
# 用于返回告示，包括重大Notice更新等相关消息

class NoticeService():

    def __init__(self):
        self.__mysqlUtil=MysqlUtil()
        self.__result=""

    # 对于默认的消息，后续可以从数据库中获取（默认的notice也会实时更新）
    def defaultChatMessage(self):
        return str("欢迎您的访问~我是阿环~为了给您提供更准确的答复，请尽量："
                   "1、登录后再提问；"
                          "2、在右侧“产品分类”中选择您要咨询的产品 ；"
                   "可以尝试输入'引导'，让机器人为你指路呦！如您对我的答案不满意，可以立即转SLA工单处理喔！")


    #用于返回告示中的notice邮件，可以将notice邮件做一个组件分类
    #同样是一个异步io操作
    '''
    component:组件类型（比如inceptor、tos之类的）
    '''
    async def componentNoticeMessage(self,component):
        result = await self.__mysqlUtil.query("select id,description,solution,esid,subassembly_name, moudle,last_modified_date from question where moudle like '%Notice%' and subassembly_name like '%" + str(component) +"%'")
        # print(type(self.__result))
        return result



    #用于返回最近最新的notice信息
    def lastNoticeMessage(self):
        return ""

if __name__ == '__main__':
    a=NoticeService().componentNoticeMessage("Hadoop")
    print(str(a))