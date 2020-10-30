#coding:utf-8

import aiomysql
import asyncio
import logging
import traceback
from config_default import configs
'''
mysql 异步版本，数据库连接池
'''

logobj = logging.getLogger('mysql')


class Pmysql:
    # 本质上这个就是一个静态变量、类变量，用来实现python环境下的单例
    __connection = None
    __pool = None


    def __init__(self):
        self.cursor = None
        self.connection = None
        # self.pool=None

    # 连接池的创建使用单例模式
    @staticmethod
    async def create_pool(loop, **kw):
        if Pmysql.__pool==None:
            try:
                logobj.info('create database connection pool...')
                # global __pool
                pool =await aiomysql.create_pool(
                    host=configs['dbpool']['host'],
                    port=configs['dbpool']['port'],
                    user=configs['dbpool']['user'],
                    password=configs['dbpool']['password'],
                    db=configs['dbpool']['db'],
                    charset=configs['dbpool']['charset'],
                    autocommit=configs['dbpool']['autocommit'],
                    maxsize=configs['dbpool']['maxsize'],
                    minsize=configs['dbpool']['minsize'],
                    loop=loop
                )
                if pool:
                    Pmysql.__pool=pool
            except:
                logobj.error('create mysql connection pool error!',exc_info=True)
            return pool
        else:
            return Pmysql.__pool

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
    # 这里做一个改动，将下面的Pmysql类封装为一个单例使用
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