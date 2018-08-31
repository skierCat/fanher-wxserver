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


class MessageWages():
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
        if('blankyear' in mydata):
            rep=re.compile('blankyear')
            mydata=rep.sub(self.content,mydata)
            fp=open(self.filename,'w')
            fp.write(mydata)
            fp.close()
            self.reply='请输入查询月份：（例如：04）'
        elif('blankmonth' in mydata):
            rep=re.compile('blankmonth')
            mydata=rep.sub(self.content,mydata)
            fp=open(self.filename,'w')
            fp.write(mydata)
            fp.close()
            myxml=ElementTree.fromstring(mydata)
            name=myxml.find('Name').text.strip(' ')
            tel=myxml.find('Tel').text.strip(' ')
            userlimit=myxml.find('Userlimit').text.strip(' ')
            year=myxml.find('Year').text.strip(' ')
            month=myxml.find('Month').text.strip(' ')
            if(len(month)==1):month=str(0)+month
            word='select wages from `members-wages` where name="'+name+'" and year="'+year+'" and month="'+month+'" and userlimit="'+userlimit+'"'
            #print(word)
            wagesdata=self.idc.searchWord(word,1)
            if(not isinstance(wagesdata,list)):
                os.remove(self.filename)
            else:
                exceptkeys=['出勤天数','双休','法定假','未出勤天数','']
                exceptvalues=['0.00','']
                self.reply=self.reply+'尊敬的'+name+'您好！\n'
                self.reply=self.reply+'您'+year+'年'+month+'月的工资明细如下\n'
                if(len(wagesdata)!=0):
                    for i in wagesdata:
                        wagesjson=eval(i[0])
                        for j in wagesjson:
                            #print(j+'-----'+wagesjson[j])
                            if((wagesjson[j]!='') and (wagesjson[j] not in exceptvalues) and (j not in exceptkeys)):
                                self.reply=self.reply+j+'：  '+wagesjson[j]+'\n'
                        #print(self.reply)
                    os.remove(self.filename)
                else:
                    self.reply='查无信息！！！'
                    os.remove(self.filename)

        else:
            if(os.path.exists(self.filename)):
                os.remove(self.filename)
        #print(self.reply)
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

            

