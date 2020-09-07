# 访问数据库，实现对象和数据库的关系映射，这里使用对象关系映射模型SQLAalchemy
import sqlalchemy
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import Session, sessionmaker

# print(sqlalchemy.__version__)
#创建数据库引擎(连接数据库) echo=True表示显示面向对象的语言转为sql语句
engine=sqlalchemy.create_engine("mysql://root:westos@localhost/Blog",
                              encoding='utf8',echo=True) #用户名、密码、主机名、数据库名


#2)建议缓存
session=sessionmaker(bind=engine)()

