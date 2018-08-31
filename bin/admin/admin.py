# -*- coding:utf-8 -*-
'''
Author: Wen
'''

import os
import json
import random
import time
import tornado.web

class AdminHandler(tornado.web.RequestHandler):
    #判断字符串是否是时间
    def is_str_time(self,string):
        try:
            time.strptime(string,"%Y-%m-%d")
            return True
        except:
            return False
    def get(self):
        type=self.get_argument("type","")
        if (type!="" and int(type)==0):
            print("登录")
            self.render("admin/admin.html")
        if (type!="" and int(type)==2):
            print("注册")
            self.render("members/register.html")
    def post(self):
        mytype=self.get_argument("type","")
        name=self.get_argument("name","")
        xmb=self.get_argument("xmb","")
        password=self.get_argument("password","")
        tel=self.get_argument("tel","")
        keypass=self.get_argument("keypass","")
        if (mytype!="" and int(mytype)==3):
            date=str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
            word='select * from yzm'
            db=myDb()
            data=db.getData(word)
            if(len(data)!=0):
                yzm=str(data[0][0])
                odate=str(data[0][1])
                if(odate==date and yzm==keypass):
                    word="select id from members where name='"+name+"' and tel='"+tel+"'"
                    odata=db.getData(word)
                    if(len(odata)==0):
                        word="INSERT INTO `members`(`name`, `tel`, `password`, `xmb`, `date`) VALUES ('"+name+"','"+tel+"','"+password+"','"+xmb+"','"+date+"')";
                        db.insertData(word)
                    db.closeData()
                elif(odate!=date and yzm==keypass):
                    yzm=random.randint(1000, 9999)
                    word="DELETE FROM `yzm` WHERE 1"
                    db.delData(word)
                    word="INSERT INTO `yzm`(`yzm`, `date`) VALUES ('"+str(yzm)+"','"+str(date)+"')";
                    db.insertData(word)
                    db.closeData()
            else:
                yzm=random.randint(1000, 9999)
                word="INSERT INTO `yzm`(`yzm`, `date`) VALUES ('"+str(yzm)+"','"+str(date)+"')";
                db.insertData(word)
                word="INSERT INTO `members`(`name`, `tel`, `password`, `xmb` ,`date`) VALUES ('"+name+"','"+tel+"','"+password+"','"+xmb+"','"+date+"')";
                db.insertData(word)
                db.closeData()
        if (mytype!="" and int(mytype)==4):
            print("正在登录")
            nowdate=str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
            id=self.get_argument("id","")
            yzpass=self.get_argument("pass","")
            word="select * from members where id='"+id+"' and password='"+yzpass+"'"
            db=myDb()
            dbdata=db.getData(word)
            if(len(dbdata)!=0):
                send_data={'id':dbdata[0][0],'dldate':nowdate,'text':'登录成功！！','key':1}
                db.closeData()
            elif(len(dbdata)==0):
                send_data={'text':'登录失败，可能是密码错误或者识别码错误！！','key':0}
                db.closeData()
            self.set_header("Content-Type","application/json;charset=UTF-8")
            self.write(json.dumps(send_data))
