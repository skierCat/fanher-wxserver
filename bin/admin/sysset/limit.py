# -*- coding:utf-8 -*-
'''
Author: Wen
'''

import json
import time
import xlrd
import random
import os
import tornado.web
from methods.webcache import myCache
from methods.webmysql import myDb
from tornado.websocket import WebSocketHandler

class LimitsetHandler(WebSocketHandler):
    #判断字符串是否是时间   
    def is_str_time(self,string):
        try:
            time.strptime(string,"%Y-%m-%d")
            return True
        except:
            return False
    def check_origin(self, origin):
        return True
    def open(self):
        pass

    def on_message(self, getdata):
        #print('gdata')
        if(type(getdata)==str):
            gdata=json.loads(getdata)
            #print(gdata)
            if('user' in gdata):
                word='select id,unitname from `system-group`'
                mydb=myDb()
                data=mydb.getData(word)
                #print(data)
                self.write_message(json.dumps(data).encode())
    def on_close(self):
        pass
        

