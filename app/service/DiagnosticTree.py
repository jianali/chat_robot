# import Mysqldb
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.dto.DiagnosticNode import DiagnosticNode
import json

a = DiagnosticNode(1,None,'根节点',[])
a.setChidNodes(DiagnosticNode(3,1,'第一层目录',[]))
a.setChidNodes(DiagnosticNode(4,1,'',[]).setChidNodes(DiagnosticNode(5,[])))

print(a.getChildNodes()[1].getId())
print(a.__dict__)
# print(json.dumps(a))

print(a.__json__())
# db = Mysqldb.connect(jdbc:mysql://172.26.4.18:3307/aiops?useUnicode=true&characterEncoding=utf8&useSSL=false)

