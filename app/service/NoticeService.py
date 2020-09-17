# 用于返回告示，包括重大Notice更新等相关消息
class NoticeService():

    # 对于默认的消息，后续可以从数据库中获取（默认的notice也会实时更新）
    def defaultChatMessage(self):
        return str("欢迎您的访问~我是阿环~为了给您提供更准确的答复，请尽量："
                   "1、登录后再提问； \n"
                          "2、在右侧“产品分类”中选择您要咨询的产品 ；\n")


    #用于返回告示中的notice邮件，可以将notice邮件做一个组件分类
    '''
    component:组件类型（比如inceptor、tos之类的）
    '''
    def componentNoticeMessage(self,component):
        return ""


    #用于返回最近最新的notice信息
    def lastNoticeMessage(self):
        return ""