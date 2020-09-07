import json
'''
数据库中包含
字段：
id，
parentId，
nodeid（一级目录的分类，用于在检索的时候构建树的时候能够减少查询量）
level（目录数的层级），
path（文章链接），
comment（备注），
filePath，
fileName，
lastModifiedDate
'''

class DiagnosticNode():
    '''
    定义一个运维诊断的树结构
    '''
    def __init__(self,id,pid,item,childNodes):
        self.id = id
        self.parentId = pid
        self.item = item
        self.childNodes = childNodes

    def setChidNodes(self,childNode):
        self.childNodes.append(childNode)
        return self

    def getChildNodes(self):
        return self.childNodes

    def getParentId(self):
        return self.parentId

    def setParentId(self,pid):
        self.parentId = pid
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

# 递归生成树结构的json文件
    def __json__(self):
        if self.childNodes==[]:
            # return {'id':self.id,'childNodes':[]}
            return ""
        else:
           childsJson=''
           for childNode in self.childNodes:
                 childsJson+=str({'id': childNode.id, 'childNodes': [childNode.__json__()]})+','
                # childsJson += str()+','
           return {'id':self.id,'childNodes':[childsJson]}
