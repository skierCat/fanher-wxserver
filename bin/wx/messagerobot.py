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
from bin.wx.msgrobot import MsgRobot
from methods.log import logRobot
from xml.etree.ElementTree import ElementTree,Element
from xml.etree import ElementTree
class MessageRobot():
    #判断字符串是否是时间
    def __init__(self,MsgType,FromUserName,ToUserName,Content):
        self.wx=FromUserName
        self.touser=ToUserName
        self.msgtype=MsgType
        self.content=Content
        self.text=[]
        self.reply=''
        self.idc=myIdc()
        #print('a')
        word="select id from `members-login` WHERE loginuser='"+self.wx+"'"
        useriddata=self.idc.searchWord(word,0)
        #print('b')
        #print(useriddata)
        if(useriddata==None):
            self.userid=0
            #print('r')
        elif(len(useriddata)==1):
            #print('c')
            self.userid=useriddata[0][0]
            #print(self.userid)
        else:
            self.userid=0
            #print('r')
    def message(self):
        #print('d')
        if(self.msgtype=='text' and ('注册' in self.content)):
            filename='tmp/'+self.wx+'.xml'
            if(os.path.exists(filename)):
                os.remove(filename)
            filename='tmp/'+self.wx+'.xml'
            rep=re.compile('注册')
            self.content=rep.sub('',self.content)
            text='<xml> <Name>blankname</Name> <Tel>blanktel</Tel> <Wx>blankwx</Wx> <Pass>blankpass</Pass> <Key>blankkey</Key></xml>'
            fp=open(filename,'w')
            fp.write(text)
            fp.close()
            self.reply="请输入您的名字："
            self.text.append(1)
            self.text.append(self.reply)
        if(self.msgtype=='text' and ('查工资' in self.content) or ('工资单' in self.content) or ('cgz' in self.content) or ('gzd' in self.content)):
            filename='tmp/'+self.wx+'wages.xml'
            if(os.path.exists(filename)):
                os.remove(filename)
            word="SELECT id FROM `members-login` WHERE loginuser='"+self.wx+"'"
            #print(word)
            data=self.idc.searchWord(word,0)
            #print(data)
            if(len(data)==1):
                word="SELECT mininame,tel,userlimit FROM `members-infor` WHERE id='"+str(data[0][0])+"'"
                #print(word)
                persondata=self.idc.searchWord(word,1)
                #print(persondata)
                #print(data)
                filename='tmp/'+self.wx+'wages.xml'
                text='<xml> <Id>'+str(data[0][0])+'</Id> <Name>'+persondata[0][0]+'</Name> <Userlimit>'+str(persondata[0][2])+'</Userlimit> <Tel>'+persondata[0][1]+'</Tel> <Year>blankyear</Year> <Month>blankmonth</Month></xml>'
                #print(text)
                fp=open(filename,'w')
                fp.write(text)
                fp.close()
                self.reply="请输入要查询年份：（例如：2018）"
                self.text.append(1)
                self.text.append(self.reply)
            else:
                self.reply='未注册！！需要注册请输入注册按照步骤完成即可。'
            self.text.append(1)
            self.text.append(self.reply)
        if((not ('注册' in self.content)) and  self.content!='查工资' and self.content!='工资单' and self.content!='cgz' and self.content!='gzd'):
            #print('g')
            robotmsg=MsgRobot(self.content,self.userid)
            robotreply=robotmsg.msg()
            replytype=robotmsg.msgtype()
            self.text.append(replytype)
            self.text.append(robotreply)
        if len(self.text)>1:
            #print('h')
            if self.text[0]==1 or self.text[0]==2:
                CreateTime = int(time.time())
                try:
                    logRobot(('发送给'+self.touser+'::'+self.text[1]))
                    output = self.reply_text(self.wx, self.touser, CreateTime, self.text[1])
                except:
                    print('messagerobot出错')
                return output
            if self.text[0]==3 or self.text[0]==4:
                CreateTime = int(time.time())
                Num=len(self.text[1][1])
                newslist=self.text[1][1]
                logRobot(('发送给'+self.touser+'::新闻'))
                output = self.reply_ptext(self.wx, self.touser, CreateTime, Num, newslist)
                return output
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
    def reply_ptext(self, FromUserName, ToUserName, CreateTime, Num, myList):
        """回复图文消息模板"""
        if(Num>1):
            outtwo=''
            textTplone = """<xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[news]]></MsgType>
            <ArticleCount>%s</ArticleCount>
            <Articles>"""
            textTpltwo="""<item>
            <Title><![CDATA[%s]]></Title>
            <Description><![CDATA[%s]]></Description>
            <PicUrl><![CDATA[%s]]></PicUrl>
            <Url><![CDATA[%s]]></Url>
            </item>"""
            textTplthree="""</Articles>
            </xml>"""
            outone = textTplone % (FromUserName, ToUserName, CreateTime, Num)
            for i in range(Num):
                outtwo=outtwo+textTpltwo % (myList[i]['article'], '', myList[i]['icon'], myList[i]['detailurl'])
            out=outone+outtwo+textTplthree
            return out
