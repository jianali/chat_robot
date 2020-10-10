import json
'''
数据库中包含
字段：
id           int          not null
  comment '引导树自己的id'
    primary key,
  parent_id    int          null
  comment '文章的父id，用于拉出检索树，用父id的目的是当前id只会存在一个父id，但是却有若干个子id，便于数据插入',
  guide_name   varchar(220) null
  comment '引导节点的简称',
  level        int          null
  comment '当前引导树处于多叉树的那个层级，用于(广度优先遍历)输出每一层的结果',
  article_id   int          null
  comment '关联表article_info，树节点对应的文章编号',
  author       varchar(20)  null
  comment '节点作者',
  publish_date timestamp    null
  comment '发布日期',
  modify_date  timestamp    null
  comment '最近修改日期'
'''

class GuideTreeInfo():
    '''
    定义一个运维诊断的树结构
    '''
    def __init__(self,id,parent_id,guide_name,level,article_id,author,publish_date,modify_date):
        self.id = id
        self.parent_id = parent_id
        self.guide_name = guide_name
        self.level=level
        self.article_id=article_id
        self.author=author
        self.publish_date=publish_date
        self.modify_date=modify_date
        self.childNodes = []

    def setChidNodes(self,childNode):
        self.childNodes.append(childNode)
        return self

    def getChildNodes(self):
        return self.childNodes

    def getParentId(self):
        return self.parent_id

    def setParentId(self,pid):
        self.parent_id = pid
        return self

    def getId(self):
        return self.id

    # 使用深度优先遍历+递归的方式构建List中的多叉树，默认当前这个self对象为根节点
    def genMultiTree(self,DiagnosticAttrMap):
        for tempId in DiagnosticAttrMap.keys():
            tempNode = DiagnosticAttrMap[tempId]
            pid = tempNode.getParentId()
            if pid is None:
                self.setChidNodes(tempNode)
            else:
                pNode = DiagnosticAttrMap[pid]
                pNode.setChidNodes(tempNode)
        return self

    # # 递归生成树结构的json文件
    # def __json__(self):
    #     return {"id":self.id,"childNodes":DiagnosticNode.child_json(self)}

    def child_json(self):
        if self.childNodes==[]:
            # return {'id':self.id,'childNodes':[]}
            return ""
        else:
           childsJson=[]
           for childNode in self.childNodes:
                     childsJson.append({"id": childNode.id, "childNodes": childNode.child_json()})
           return childsJson




