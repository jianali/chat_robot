# import Mysqldb
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.model.GuideTreeInfo import GuideTreeInfo
import json

class DiagnosticTree:

    # a = DiagnosticNode(1,None,'根节点',[])
    # a.setChidNodes(DiagnosticNode(3,1,'第一层目录',[]))
    # a.setChidNodes(DiagnosticNode(4,1,'第一层目录',[]).setChidNodes(DiagnosticNode(5,4,'第二层目录',[])))

    # print(a.getChildNodes()[1].getId())
    # print(a.__dict__)
    # # print(json.dumps(a))
    # # 测试可以正常返回json结构的多叉树
    # print(json.dumps(a.__json__()))


    #测试解析json数据结构部分
    #并打印出相关树状结构，可以封装为一个ul和li的结构，包装在div里面返回给前端
    # testjson = json.dumps(a.__json__())
    # 转换为字典格式
    # outjson = json.loads(testjson)
    # print("输出字典格式的json")

    def child_json(node):
        if node.childNodes == []:
            return ""
        else:
            childsJson = ""
            for childNode in node.childNodes:
                childsJson +="<ul>"+ "<li>"+str(childNode.id)+"</li>"+DiagnosticTree.child_json(childNode)+"</ul>"
            return childsJson

    # print(child_json(a))
    def toHtml(nodes):
        return "<ul>"+ "<li>"+str(nodes.id)+"</li>"+DiagnosticTree.child_json(nodes)+"</ul>"

    # print(str(outjson))






# db = Mysqldb.connect(jdbc:mysql://172.26.4.18:3307/aiops?useUnicode=true&characterEncoding=utf8&useSSL=false)

