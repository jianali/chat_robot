#config_default.py
import logging

configs = {
    'dbpool':{
        'host':'172.26.4.18',
        'port':3307,
        'user':'root',
        'password':'',
        'db':'aiops',
        'charset':'utf8',
        'autocommit':True,
        'maxsize':10,
        'minsize':1
    },
    'log':{
        'path':'./chatrobot.log',
        'level':logging.INFO
    }
}
