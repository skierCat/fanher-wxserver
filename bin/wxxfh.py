# -*- coding:utf-8 -*-
'''
Author: Wen
'''

import os
import json
import random
import time
import tornado.web
import hashlib
from methods.log import logRobot
from bin.wx.messageregist import MessageRegist
from bin.wx.messagewages import MessageWages
from bin.wx.messagerobot import MessageRobot
from xml.etree import ElementTree as ET


class WxxfhHandler(tornado.web.RequestHandler):
    #判断字符串是否是时间   
    def is_str_time(self,string):
        try:
            time.strptime(string,"%Y-%m-%d")
            return True
        except:
            return False
    def get(self):
        signature = self.get_argument('signature','')
        timestamp = self.get_argument('timestamp','')
        nonce = self.get_argument('nonce','')
        echostr = self.get_argument('echostr','')
        #print('微信sign校验,signature='+signature+',&timestamp='+timestamp+'&nonce='+nonce+'&echostr='+echostr)
        result = self.check_signature(signature, timestamp, nonce)
        if result:
            print('微信sign签名成功！！')
            #print('微信sign签名成功！！,返回echostr='+echostr)
            self.write(echostr)
        else:
            print('微信sign签名失败！！')
    def post(self):
        body = self.request.body
        data = ET.fromstring(body)
        if(data.find('Content')!=None):
            logRobot('微信消息回复中心=>收到用户消息  ' + data.find('FromUserName').text+ ' : ' + data.find('Content').text)
        ToUserName = data.find('ToUserName').text
        FromUserName = data.find('FromUserName').text
        MsgType = data.find('MsgType').text
        filename='tmp/'+FromUserName+'.xml'
        filenamewages='tmp/'+FromUserName+'wages.xml'
        if MsgType == 'text' or MsgType == 'voice':
            '''文本消息 or 语音消息'''
            try:
                MsgId = data.find("MsgId").text
                if MsgType == 'text':
                    Content = data.find('Content').text  # 文本消息内容
                elif MsgType == 'voice':
                    Content = data.find('Recognition').text  # 语音识别结果，UTF8编码
                if Content!='' and os.path.exists(filename):
                    replycode = MessageRegist(MsgType,FromUserName,ToUserName,Content,filename)
                    reply_content=replycode.message()
                elif Content!='' and os.path.exists(filenamewages):
                    replycode = MessageWages(MsgType,FromUserName,ToUserName,Content,filenamewages)
                    reply_content=replycode.message()
                    #print(reply_content)
                elif Content!='' and (not os.path.exists(filename)) and (not os.path.exists(filenamewages)):
                    replycode = MessageRobot(MsgType,FromUserName,ToUserName,Content)
                    reply_content=replycode.message()
                else:
                    # 查找不到关键字,默认回复
                    #print('到这里g')
                    msgcontent = "客服小儿智商不够用啦~"
                    CreateTime = int(time.time())
                    out = self.reply_text(FromUserName, ToUserName, CreateTime, msgcontent)
                if reply_content!='':
                    self.write(reply_content)
            except:
                pass
        elif MsgType == 'event':
            '''接收事件推送'''
            try:
                Event = data.find('Event').text
                if Event == 'subscribe':
                    # 关注事件
                    CreateTime = int(time.time())
                    reply_content = '您已关注小小饭盒微信公众号，本号码提供财务部工资查询，以及智能聊天功能，请输入【注册】，并按照步骤进行下一步！！'
                    self.logtocontrol('向用户'+ToUserName+'发送了：'+reply_content)
                    out = self.reply_text(FromUserName, ToUserName, CreateTime, reply_content)
                    self.write(out)
            except:
                pass   
    def check_signature(self, signature, timestamp, nonce):
        """校验token是否正确"""
        token = 'myxfh'
        L = [timestamp, nonce, token]
        L.sort()
        s = L[0] + L[1] + L[2]
        sha1 = hashlib.sha1(s.encode('utf-8')).hexdigest()
        #print('sha1=' + sha1 + '&signature=' + signature)
        return sha1 == signature
    def reply_text(self, FromUserName, ToUserName, CreateTime, Content):
        """回复文本消息模板"""
        textTpl = """<xml> <ToUserName><![CDATA[%s]]></ToUserName> <FromUserName><![CDATA[%s]]></FromUserName> <CreateTime>%s</CreateTime> <MsgType><![CDATA[%s]]></MsgType> <Content><![CDATA[%s]]></Content></xml>"""
        out = textTpl % (FromUserName, ToUserName, CreateTime, 'text', Content)
        return out
    def logtocontrol(self,Logtext):
        """将所有的日志输出到我的微信"""
        xfhUsername='gh_ec7550e89a58'
        mywxUsername='oo28KwWwLRc6lqDewkRz9TSNe8SY'
        CreateTime = int(time.time())
        out = self.reply_text(mywxUsername,xfhUsername, CreateTime, Logtext)
        self.write(out)

            

