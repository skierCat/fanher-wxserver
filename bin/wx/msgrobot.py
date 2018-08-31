# -*- coding:utf-8 -*-
'''
Author: Wen
'''

import os
import random
import time
import requests
from methods.webidc import myIdc
class MsgRobot():
    def __init__(self,text,userid):
        self.text=text
        self.userid=userid
        self.type=0
        self.reply=''
        self.key='df7f59d8ff184ea685065a9ab94effc5'
        self.url='http://www.tuling123.com/openapi/api'
        self.idc=myIdc()
    def msg(self):
        if(self.userid!=0):
            data={'key':''+self.key+'','info':''+self.text+'','userid':''+str(self.userid)+''}
            sendpost=requests.post(self.url,data=data)
            mytext=sendpost.json()
            #print('导致了')
            if(mytext['code']==100000):
                self.type=1
                self.reply=mytext['text']
                word="select ques from `chat-dilog` where answer='"+self.reply+"'"
                #print('导致了')
                #print(word)
                data=self.idc.searchWord(word,0)
                #print(data)
                if(data==None):
                    #print('导致了')
                    word="INSERT INTO `chat-dilog`(`ques`, `answer`) VALUES ('"+self.text+"','"+self.reply+"')"
                    self.idc.insertWord(word,0)
                    #print('导致了')
            elif(mytext['code']==200000):
                self.type=2
                self.reply=mytext['text']+'\n'+mytext['url']
            elif(mytext['code']==302000):
                self.type=3
                ptext=[]
                self.reply=mytext['text']
                list=mytext['list']
                ptext.append(self.reply)
                ptext.append(list)
            elif(mytext['code']==308000):
                ptext=[]
                self.type=4
                self.reply=mytext['text']
                list=mytext['list']
                ptext.append(self.reply)
                ptext.append(list)
            if(self.type==1 or self.type==2):
                return self.reply
            elif(self.type==3 or self.type==4):
                return ptext
    def msgtype(self):
        if(self.userid!=0):
            return self.type
if __name__ == '__main__':
    mymsg=MsgRobot('你好',12)
    mymsg.msg()
    

            

