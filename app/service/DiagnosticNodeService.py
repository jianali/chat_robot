# 访问数据库，实现对象和数据库的关系映射，这里使用对象关系映射模型SQLAalchemy
import sqlalchemy
from sqlalchemy import Column,Integer,String,VARCHAR
from sqlalchemy.orm import Session, sessionmaker

from sqlalchemy.ext.declarative import declarative_base

# print(sqlalchemy.__version__)
#创建数据库引擎(连接数据库) echo=True表示显示面向对象的语言转为sql语句
engine=sqlalchemy.create_engine("mysql://root@172.26.4.18:3307/aiops",
                              encoding='utf8',echo=True) #用户名、密码、主机名、数据库名
# 2)建议缓存
session = sessionmaker(bind=engine)()
# 3)创建数据库对象需要继承的基类
Base = declarative_base()


# 3）创建类==数据库表
class diagnostic_tree(Base):  # 父类为Base才能将面向对象的语言转为sql语句。写表结构信息
    # 数据库表名称
    __tablename__ = 't_diagnostic_tree'
    # 数据库表属性信息
    id = Column(Integer, primary_key=True, autoincrement=True)
    tree_name = Column(VARCHAR(220))

    def __repr__(self):
        return str(self.id)+","+self.tree_name #返回对象绑定的属性：tree_name、id


if __name__ == '__main__':
    print(session.query(diagnostic_tree).all())


