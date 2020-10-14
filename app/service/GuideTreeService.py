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
        result=await self.__mysqlUtil.query("select a.id,a.parent_id,a.guide_name,a.level,a.article_id,a.author,a.publish_date,a.modify_date,b.title from guidetree_info a left join t_product_publication b on a.article_id=b.id where a.id="+str(id) )
        # print(type(self.__result))
        return result

    # 删除节点
    async def deleteNode(self,id):
        try:
        # if not isinstance(id,int):
        #     raise ValueError('id must be an integer,请检查传入的参数必须为数字id')
            result=await self.__mysqlUtil.query("delete from guidetree_info where id=%s" % (id,) )
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
        result=await self.__mysqlUtil.query("select a.id,a.parent_id,a.guide_name,a.level,a.article_id,a.author,a.publish_date,a.modify_date,b.title from guidetree_info a left join t_product_publication b on a.article_id=b.id where parent_id="+str(pid))
        # print(type(self.__result))
        return result

    def listToDict(self,input):
        root={}
        lookup={}
        root['name'] = 'rootnode';
        lookup[0] = root
        for item in input:
            if item['parent_id'] in lookup.keys():
                node={'name':item['guide_name'],'id':item['id']}
                lookup[item['parent_id']].setdefault('children',[]).append(node)
                lookup[item['id']]=node
        return root

    # 使用算法，加载出所有的目录树
    async def getGuideTrees(self, id):
        guidetreesresult = await self.__mysqlUtil.query("select * from guidetree_info order by id")
        # print(type(self.__result))
        guidemap=OrmUtil.toMap(guidetreesresult,
                      ["id", "parent_id",
                       "guide_name", "level",
                       "article_id", "author",
                       "publish_date",
                       "modify_date"])
        result=self.listToDict(guidemap)
        # guideinfomaps={}
        # for guideitem in guidemap:
        #     tmp=GuideTreeInfo("","","","","","","","")
        #     tmp.__dict__=guideitem
        #     tmp.childNodes=[]
        #     guideinfomaps[tmp.id]=tmp
        # # 开始重构以id为首的树形结构
        # guidetree=guideinfomaps[id]
        # for tempId in guideinfomaps.keys():
        #     tempNode = guideinfomaps[tempId]
        #     pid = tempNode.getParentId()
        #     if pid!=0 and pid in guideinfomaps.keys():
        #         pNode = guideinfomaps[pid]
        #         pNode.childNodes.append(tempNode)
        # bbb=guideinfomaps[id].__dict__
        #
        # result=json.dumps(guideinfomaps[id].__dict__, cls=DateEncoder)
        # 进一步将数组转换为DiagnosticNode对象
        # json.dumps({'resultdesc': 'Notice相关信息如下：', 'resultdata': OrmUtil.toMap(guideNodeResult,
        #                                                                        ["id", "parent_id",
        #                                                                         "guide_name", "level",
        #                                                                         "article_id", "author",
        #                                                                         "publish_date",
        #                                                                         "modify_date"])}, cls=DateEncoder)
        # for node in result：

        # guidetreeclass=json.loads(result)
        # result=json.dumps(result)
        if(int(id)!=0):
            result=list(filter(lambda x:x['id']==int(id),result['children']))[0]
        return json.dumps(result)

    # 修改节点信息，传入参数为一个json串
    async def modifyNode(self,args):
        await self.__mysqlUtil.query("update guidetree_info set guide_name='"+str(args['guidename'])+"' where id="+str(args['id']))
        return "success"

    async def insertNode(self,args):

        if args['article_id']=='':
            args['article_id']='null'
        args.setdefault('article_id', 'null')
        args.setdefault('level', 3)
        print("insert into guidetree_info(parent_id,guide_name,level,article_id,author,publish_date,modify_date) "
              "value ({pid},'{guide_name}',{level},{article_id},'{author}','{publish_date}','{modify_date}')"
              .format(pid=args['pid'], guide_name=args['guidename'], level=3, article_id=args['article_id'],
                      author='lj', publish_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                      modify_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        await self.__mysqlUtil.query("insert into guidetree_info(parent_id,guide_name,level,article_id,author,publish_date,modify_date) "
                                     "value ({pid},'{guide_name}',{level},{article_id},'{author}','{publish_date}','{modify_date}')"
            .format(pid=args['pid'],guide_name=args['guidename'],level=3,article_id=args['article_id'],author='lj',publish_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),modify_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        return "success"

    async def getArticleList(self,title,components,product_type):
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
