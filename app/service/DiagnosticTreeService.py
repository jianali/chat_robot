# 用于返回各个运维诊断树，在聊天记录中可查看
#这个服务涉及两张表，t_DiagnosticTree和t_Diagnostic_item


from app.dto.DiagnosticTreeDto import DiagnosticTreeDto
from app.util.MysqlUtil import MysqlUtil

class DiagnosticTreeService():
    '''
    定义一个运维诊断树的查询插入等功能的服务器
    '''

    def __init__(self):
        self.__mysqlUtil=MysqlUtil()
        self.__result=None

# 返回所有的运维结构树
    def getDiagnosticTreeAll(self):
        self.__result=self.__mysqlUtil.querysql("select * from t_diagnostic_item order by tree_id,id")
        print(type(self.__result))
        return self.__result

# 返回单个组件的运维结构树,传入参数为组件名称
    def getDiagnosticTree(self,componentName):

        self.__result = self.__mysqlUtil.querysql("select a.* from t_diagnostic_item a ,t_diagnostic_tree b where b.tree_name="+componentName+" and a.tree_id=b.id order by a.id;")
        print(type(self.__result))
        return self.__result

# 显示诊断树中的组件
    def getDiagnosticTreeNames(self):
        self.__result = self.__mysqlUtil.querysql("select * from t_diagnostic_tree sort by ")
        print(type(self.__result))
        return self.__result


