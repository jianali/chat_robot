#coding:utf-8

import aiomysql
import asyncio
import logging
import traceback
'''
mysql 异步版本，后续可以改成数据库连接池
'''

logobj = logging.getLogger('mysql')

class Pmysql:
    __connection = None

    def __init__(self):
        self.cursor = None
        self.connection = None

    @staticmethod
    async def getconnection():
        if Pmysql.__connection == None:
            conn = await aiomysql.connect(
                host='172.26.4.18',
                port=3307,
                user='root',
                password='',
                db='aiops',
                )
            if conn:
                Pmysql.__connection = conn
                return conn
            else:
                raise("connect to mysql error ")
        else:
            return Pmysql.__connection

    async def query(self,query,args=None):
        self.cursor = await self.connection.cursor()
        await self.cursor.execute(query,args)
        r = await self.cursor.fetchall()
        await self.cursor.close()
        return r



class MysqlUtil:
    # 测试
    async def ceshi(self):
        conn = await Pmysql.getconnection()
        mysqlobj.connection = conn
        await conn.ping()
        r = await mysqlobj.query("select * from t_diagnostic_item")
        for i in r:
            print(i)
        conn.close()

    # 查询操作
    async def query(self,sql):
        mysqlobj = Pmysql()
        conn = await Pmysql.getconnection()
        mysqlobj.connection = conn
        await conn.ping()
        r = await mysqlobj.query(sql)
        for i in r:
            print(i)
        conn.close()
        return r


    def querysql(self,sql):
        loop = asyncio.get_event_loop()
        mysqlutil=MysqlUtil()
        return loop.run_until_complete(mysqlutil.query(sql))


if __name__ == '__main__':
    mysqlobj = Pmysql()
    loop = asyncio.get_event_loop()
    mysqlutil=MysqlUtil()
    loop.run_until_complete(mysqlutil.query("select * from t_diagnostic_item"))