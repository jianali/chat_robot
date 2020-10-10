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
    async def create_pool(loop, **kw):
        # logging.info('create database connection pool...')
        global __pool
        __pool =await aiomysql.create_pool(
            host=kw.get('host', '172.26.4.18'),
            port=kw.get('port', 3307),
            user=kw['user'],
            password=kw['password'],
            db=kw['db'],
            charset=kw.get('charset', 'utf8'),
            autocommit=kw.get('autocommit', True),
            maxsize=kw.get('maxsize', 10),
            minsize=kw.get('minsize', 1),
            loop=loop
        )
        return __pool

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
        # conn = await Pmysql.getconnection()
        loop = asyncio.get_event_loop()
        pool= await Pmysql.create_pool(loop,user='root',password='',db='aiops')
        async with pool.acquire() as conn:
        # # mysqlobj.connection = conn
        #     await conn.ping()
        #     r = await mysqlobj.query(sql)
        #     for i in r:
        #         print(i)
        #     conn.close()
            async with conn.cursor() as cur:
                await cur.execute(sql)
                r = await cur.fetchall()
            print(r)
        return r


    def querysql(self,sql):
        # sanic的路由本质上就是一个异步的，这边调用sql也是异步的话，会导致抢占event loop（所以这个函数只是测试使用）
        loop = asyncio.get_event_loop()
        mysqlutil=MysqlUtil()
        result=loop.run_until_complete(mysqlutil.query(sql,loop))
        # loop.close()
        return result


# 更改使用数据库连接池的方式
if __name__ == '__main__':
    mysqlobj = Pmysql()
    loop = asyncio.get_event_loop()
    mysqlutil=MysqlUtil()
    loop.run_until_complete(mysqlutil.query("select * from guidetree_info",loop))