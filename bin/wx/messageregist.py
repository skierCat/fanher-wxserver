# -*- coding:utf-8 -*-
'''
Author: Wen
'''

import os
import re
import random
import time
import tornado.web
import hashlib
from methods.webidc import myIdc
from xml.etree.ElementTree import ElementTree,Element
from xml.etree import ElementTree


class MessageRegist():
    #判断字符串是否是时间
    def __init__(self,MsgType,FromUserName,ToUserName,Content,filename):
        self.wx=FromUserName
        self.msgtype=MsgType
        self.content=Content
        self.filename=filename
        self.touser=ToUserName
        self.text=[]
        self.reply=''
        self.idc=myIdc()
    def message(self):
        file=open(self.filename)
        mydata=file.read()
        file.close()
        if('blankname' in mydata):
            rep=re.compile('blankname')
            mydata=rep.sub(self.content,mydata)
            fp=open(self.filename,'w')
            fp.write(mydata)
            fp.close()
            self.reply='请输入您的手机号：'
        elif('blanktel' in mydata):
            rep=re.compile('blanktel')
            mydata=rep.sub(self.content,mydata)
            fp=open(self.filename,'w')
            fp.write(mydata)
            fp.close()
            self.reply='请输入您想到的任何句子：'
        elif('blankwx' in mydata):
            rep=re.compile('blankwx')
            mydata=rep.sub(self.wx,mydata)
            fp=open(self.filename,'w')
            fp.write(mydata)
            fp.close()
            self.reply='请输入您想设置的密码：'
        elif('blankpass' in mydata):
            rep=re.compile('blankpass')
            word='select id,unitname from `system-group` where 1'
            xmb=self.idc.searchWord(word,0)
            mydata=rep.sub(self.content,mydata)
            fp=open(self.filename,'w')
            fp.write(mydata)
            fp.close()
            self.reply='请回复项目部名前的数字选择项目部：\n'
            for i in xmb:
                for j in i:
                    if(isinstance(j,str)):
                        self.reply=self.reply+j
                    else:
                        self.reply=self.reply+str(j)+'、'
                self.reply=self.reply+'\n'
        elif('blankkey' in mydata):
            rep=re.compile('blankkey')
            mydata=rep.sub(self.content,mydata)
            fp=open(self.filename,'w')
            fp.write(mydata)
            fp.close()
            myxml=ElementTree.fromstring(mydata)
            date=str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
            name=myxml.find('Name').text.strip(' ')
            tel=myxml.find('Tel').text.strip(' ')
            wx=myxml.find('Wx').text.strip(' ')
            sha256 = hashlib.sha256()
            mypass=myxml.find('Pass').text.strip(' ')
            sha256.update(mypass.encode('utf-8'))
            mypass = sha256.hexdigest()
            keypass=myxml.find('Key').text.strip(' ')
            word='SELECT id FROM `members-infor` WHERE tel="'+tel+'" and mininame="'+name+'"'
            data=self.idc.searchWord(word,0)
            if(data==None):
                if(name!='' and mypass!='' and tel!=''):
                    word="insert into `members-infor` (mininame,tel,pass,userlimit,date,userlevel) VALUES ('"+name+"','"+tel+"','"+mypass+"','"+keypass+"','"+date+"','0')"
                    self.idc.insertWord(word,0)
                    word='select id from `members-login` where loginuser="'+wx+'"'
                    tmpdata=self.idc.searchWord(word,0)
                    word='select id from `members-login` where loginuser="'+tel+'"'
                    tmpteldata=self.idc.searchWord(word,0)
                    word='select id from `members-infor` where tel="'+tel+'"'
                    iddata=self.idc.searchWord(word,0)
                    if(tmpdata==None and len(iddata)==1):
                        word='INSERT INTO `members-login`(`id`,`loginuser`) VALUES ("'+str(iddata[0][0])+'","'+wx+'")'
                        self.idc.insertWord(word,0)
                    if(tmpteldata==None and len(iddata)==1):
                        word='INSERT INTO `members-login`(`id`,`loginuser`) VALUES ("'+str(iddata[0][0])+'","'+tel+'")'
                        self.idc.insertWord(word,0)
                    self.reply='完成注册！！' 
                    os.remove(self.filename)
                else:
                    self.reply='您输入的信息有不合规的，请重新注册！！' 
                    os.remove(self.filename)
            else:
                self.reply='您已经注册过了！！'
                if(os.path.exists(self.filename)):
                    os.remove(self.filename)
        else:
            fp=open(self.filename,'w')
            fp.write(mydata)
            fp.close()
            myxml=ElementTree.fromstring(mydata)
            date=str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
            name=myxml.find('Name').text.strip(' ')
            tel=myxml.find('Tel').text.strip(' ')
            wx=myxml.find('Wx').text.strip(' ')
            sha256 = hashlib.sha256()
            mypass=myxml.find('Pass').text.strip(' ')
            sha256.update(mypass.encode('utf-8'))
            mypass = sha256.hexdigest()
            keypass=myxml.find('Key').text.strip(' ')
            word='SELECT id FROM `members-infor` WHERE tel="'+tel+'" and mininame="'+name+'"'
            data=self.idc.searchWord(word,0)
            if(data==None):
                if(name!='' and mypass!='' and tel!=''):
                    word="insert into `members-infor` (mininame,tel,pass,userlimit,date,userlevel) VALUES ('"+name+"','"+tel+"','"+mypass+"','"+keypass+"','"+date+"','0')"
                    self.idc.insertWord(word,0)
                    word='select id from `members-login` where loginuser="'+wx+'"'
                    tmpdata=self.idc.searchWord(word,0)
                    word='select id from `members-login` where loginuser="'+tel+'"'
                    tmpteldata=self.idc.searchWord(word,0)
                    word='select id from `members-infor` where tel="'+tel+'"'
                    iddata=self.idc.searchWord(word,0)
                    if(tmpdata==None and len(iddata)==1):
                        word='INSERT INTO `members-login`(`id`,`loginuser`) VALUES ("'+str(iddata[0][0])+'","'+wx+'")'
                        self.idc.insertWord(word,0)
                    if(tmpteldata==None and len(iddata)==1):
                        word='INSERT INTO `members-login`(`id`,`loginuser`) VALUES ("'+str(iddata[0][0])+'","'+tel+'")'
                        self.idc.insertWord(word,0)
                    self.reply='完成注册！！' 
                    os.remove(self.filename)
                else:
                    self.reply='您输入的信息有不合规的，请重新注册！！' 
                    os.remove(self.filename)
            else:
                self.reply='您已经注册过了！！'
                if(os.path.exists(self.filename)):
                    os.remove(self.filename)
        self.text.append(1)
        self.text.append(self.reply)
        if len(self.text)>1:
            if self.text[0]==1:
                CreateTime = int(time.time())
                out = self.reply_text(self.wx, self.touser, CreateTime, self.text[1])
                return out
    def read_xml(self,in_path):
        tree=ElementTree()
        tree.parse(in_path)
        return tree
    def write_xml(self,tree,out_path):
        tree.write(out_path,encoding="utf-8",xml_declaration=True)
    def change_node_text(self,nodelist,text,is_add=False,is_delete=False):
       '''''改变/增加/删除一个节点的文本
       nodelist:节点列表
       text : 更新后的文本'''
       for node in nodelist:
            if is_add:
                node.text+=text
            elif is_delete:
                node.text=""
            else:
                node.text=text
    def reply_text(self, FromUserName, ToUserName, CreateTime, Content):
        """回复文本消息模板"""
        textTpl = """<xml> <ToUserName><![CDATA[%s]]></ToUserName> <FromUserName><![CDATA[%s]]></FromUserName> <CreateTime>%s</CreateTime> <MsgType><![CDATA[%s]]></MsgType> <Content><![CDATA[%s]]></Content></xml>"""
        out = textTpl % (FromUserName, ToUserName, CreateTime, 'text', Content)
        return out

            

