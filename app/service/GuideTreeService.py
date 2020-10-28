from app.model.GuideTreeInfo import GuideTreeInfo
from app.util.OrmUtil import OrmUtil
from app.util.MysqlUtil import MysqlUtil

from app.util.DateEncoder import DateEncoder
import json
import asyncio
import datetime

class GuideTreeService():
    '''
    用于机器人引导，返回数据库中的相关引导信息，数据库也是异步操作
    '''

    def __init__(self):
        self.__mysqlUtil=MysqlUtil()
        self.__result=""

    # 返回相关的引导信息，传入的参数是一个id
    # 也是一个异步IO的操作，本质上是只有一个eventloop的
    async def getNode(self,id):
        # if not isinstance(id,int):
        #     raise ValueError('id must be an integer,请检查传入的参数必须为数字id')
        result=await self.__mysqlUtil.query("select a.id,a.parent_id,a.guide_name,a.article_id,a.author,a.publish_date,a.modify_date,b.title "
                                            "from guidetree_info a left join t_product_publication b "
                                            "on a.article_id=b.id where state=1 and a.id={id}"
                                            .format(id=str(id)))
        # print(type(self.__result))
        nodemap=OrmUtil.toMap(result,
                      ["id", "parent_id",
                       "guide_name",
                       "article_id", "author",
                       "publish_date",
                       "modify_date", "title"])
        return nodemap

    # 删除节点
    async def deleteNode(self,id):
        try:
        # if not isinstance(id,int):
        #     raise ValueError('id must be an integer,请检查传入的参数必须为数字id')
        #     result=await self.__mysqlUtil.query("delete from guidetree_info where id=%s" % (id,) )
            result = await self.__mysqlUtil.query("update guidetree_info set state=0 where id={id}".format(id=id))
        # print(type(self.__result))
            result='success'
        except Exception as e:
            print(e)
            result='failed'
        finally:
            return result

    async def getRootNode(self,pid):
        # if not isinstance(id,int):
        #     raise ValueError('id must be an integer,请检查传入的参数必须为数字id')
        result=await self.__mysqlUtil.query("select a.id,a.parent_id,a.guide_name,a.article_id,a.author,a.publish_date,a.modify_date,b.title "
                                            "from guidetree_info a left join t_product_publication b "
                                            "on a.article_id=b.id "
                                            "where parent_id={pid} and state=1"
                                            .format(pid=str(pid)))
        rootmap=OrmUtil.toMap(result,
                      ["id", "parent_id",
                       "guide_name",
                       "article_id", "author",
                       "publish_date",
                       "modify_date","title"])
        # print(type(self.__result))
        return rootmap

    def listToDict(self,input):
        # root={}
        # lookup={}
        # root['name'] = 'rootnode';
        # lookup[0] = root
        # for item in input:
        #     if item['parent_id'] in lookup.keys():
        #         node={'name':item['guide_name'],'id':item['id']}
        #         lookup[item['parent_id']].setdefault('children',[]).append(node)
        #         lookup[item['id']]=node

# 下面是使用递归的实现方式，深度优先遍历
        lookup={}
        for item in input:
            node = {'name': item['guide_name'], 'id': item['id']}
            lookup.setdefault(item['parent_id'],[])
            lookup[item['parent_id']].append(node)

        def child(childnode):
            if childnode['id'] in lookup.keys():
                arr=[]
                for item in lookup[childnode['id']]:
                    arr.append({'name':item['name'],'id':item['id'],'children':child({'id':item['id']})})
                return arr
            else:
                return []
        root={'name':'rootnode','children':child({'id':0})}

        return root

    # 使用算法，加载出所有的目录树
    async def getGuideTrees(self, id):
        guidetreesresult = await self.__mysqlUtil.query("select * from guidetree_info where state=1 order by id,parent_id")
        # print(type(self.__result))
        result=[]
        if len(guidetreesresult)>0:
            guidemap=OrmUtil.toMap(guidetreesresult,
                          ["id", "parent_id",
                           "guide_name", "level",
                           "article_id", "author",
                           "publish_date",
                           "modify_date"])
            result=self.listToDict(guidemap)
            if(int(id)!=0):
                result=list(filter(lambda x:x['id']==int(id),result['children']))[0]
        return json.dumps(result)

    # 修改节点信息，传入参数为一个json串
    async def modifyNode(self,args):
        # 关于里面的键值校验是否为空，这个里面感觉是可以做成一个工具方法
        if args['article_id']=='':
            args['article_id']='null'
        await self.__mysqlUtil.query("update guidetree_info set guide_name='{guidename}',"
                                     "article_id='{articleid}',"
                                     "parent_id='{pid}',"
                                     "modify_date='{modifydata}' where id={id}"
                                     .format(id=str(args['id']),guidename=str(args['guidename']),articleid=str(args['article_id']),pid=args['pid'],modifydata=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        return "success"

    # 保存聊天记录
    async def saveChatHistory(self,args):
        await self.__mysqlUtil.query("insert into chat_history(recordtext,author,publish_date)"
                                     "value ('{recordtext}','{author}','{publish_date}')"
                                     .format(recordtext=str(args['messages'][-1]).replace("'","").replace('"','').replace(',',''),author=args['author'],publish_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        return "success"


    async def insertNode(self,args):

        if args['article_id']=='':
            args['article_id']='null'
        args.setdefault('article_id', 'null')
        await self.__mysqlUtil.query("insert into guidetree_info(parent_id,guide_name,state,article_id,author,publish_date,modify_date) "
                                     "value ({pid},'{guide_name}','{state}',{article_id},'{author}','{publish_date}','{modify_date}')"
            .format(pid=args['pid'],guide_name=args['guidename'],state=1,article_id=args['article_id'],author=args['author'],publish_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),modify_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        return "success"


    async def getArticleList(self,title,components,product_type):
        result=[]
        if(len(components)!=0):
            result = await self.__mysqlUtil.query(
                "select id,title from t_product_publication where components='{components}'".format(components=components))
        elif(len(product_type)!=0):
            result = await self.__mysqlUtil.query(
                "select id,title from t_product_publication where publication_type='{product_type}'".format(product_type=product_type))
        elif(len(title)!=0):
            result = await self.__mysqlUtil.query("select id,title from t_product_publication where title like '%{title}%'".format(title=title))
        articlelist = OrmUtil.toMap(result,["id", "title"])
        return articlelist

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    result=loop.run_until_complete(GuideTreeService().getGuideTrees(1))
    print(result)
