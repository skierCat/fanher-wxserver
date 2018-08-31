# -*- coding:utf-8 -*-
'''
Author: Wen
'''

import hashlib
import json
import time
import tornado.web
from methods.webcache import myCache
from methods.webmysql import myDb
from tornado.websocket import WebSocketHandler

class LoginHandler(WebSocketHandler):
    def check_origin(self, origin):  
        return True
    def open(self):
        pass

    def on_message(self, getdata):
        logininfo=json.loads(getdata)
        sha256 = hashlib.sha256()
        sha256.update(logininfo[0]['pwd'].encode('utf-8'))
        passwordsha = sha256.hexdigest()
        word='select id from `members-login` where loginuser = "'+logininfo[0]['user']+'"'
        print(word)
        mydb=myDb()
        getdata=mydb.getData(word)
        print(getdata)
        word='select pass,userlimit,userlevel,mininame from `members-infor` where id = "'+str(getdata[0][0])+'"'
        print(word)
        getdata=mydb.getData(word)
        print(getdata)
        if(getdata[0][0]==passwordsha):
            loginsend={}
            loginsend['onlineuser']=logininfo[0]['user']
            loginsend['mininame']=getdata[0][3]
            loginsend['userlimit']=getdata[0][1]
            loginsend['userlevel']=getdata[0][2]
            loginsend['time']=time.time()
            cache=myCache()
            random=cache.randomkey()
            online=random+'_'+cache.dataconfig['db']+'_'+'onlineuser'+'_user'+'_'
            online=online+logininfo[0]['user']+'_0'
            #print(online)
            onlinedata={}
            onlinedata[online]=time.time()
            temp=cache.createCache(onlinedata)
            self.write_message(json.dumps(loginsend).encode())
            #print(json.dumps(loginsend))

    def on_close(self):
        pass

