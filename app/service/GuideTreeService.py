from app.util.MysqlUtil import MysqlUtil

class GuideTreeService():
    '''
    用于机器人引导，返回数据库中的相关引导信息，数据库也是异步操作
    '''

    def __init__(self):
        self.__mysqlUtil=MysqlUtil()
        self.__result=""

    # 返回相关的引导信息，传入的参数是一个id
    # 也是一个异步IO的操作，本质上是只有一个eventloop的
    async def getGuideTree(self,id):
        result=await self.__mysqlUtil.query("select * from guidetree_info where parent_id="+str(id))
        # print(type(self.__result))
        return result
