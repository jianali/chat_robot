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

class DiagnosticTreeDto():
    '''
    定义一个运维诊断的树结构
    '''
    def __init__(self,id,diagnostic_item_name,diagnostic_tree,tree_name):
        self.id = id
        self.diagnostic_item_name = diagnostic_item_name
        self.diagnostic_tree = diagnostic_tree
        self.tree_name = tree_name



