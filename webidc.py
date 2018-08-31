# -*- coding:utf-8 -*-
'''
Author: Feng Wenqiang
E-mail: hoontu@sina.com
'''
import pymysql
import redis
import os
import re
from methods.webmysql import myDb
from methods.webcache import myCache

class myIdc():
    def __init__(self):
        self.mydb=myDb()
        self.mycache=myCache()
    def searchWord(self,words,typenum):
        #word查询语句
        #typenum为0，按语句直接查询mysql，为1开启cache混合查询，为2只查询cache
        if(typenum==1):
            searchkeys=[]#搜索的键
            searchforms=[]#搜索的表
            searchtips=[]#搜索的条件
            searchtipsconn=[]#搜索的条件连接符
            values=[]#搜索表和键后得到的redis值
            resultpop=[]#最终结果
            key=re.split(r'[\`\s+]',words)
            tmp=0
            for i in key:
                tmpkg=0
                if(i=='select' or i=='SELECT'):
                    tmpkg=1
                    tmp=1
                if(i=='from' or i=='FROM'):
                    tmpkg=1
                    tmp=2
                if(i=='where' or i=='WHERE'):
                    tmpkg=1
                    tmp=3
                if((i=='or' or i=='and') and i!=''):
                    searchtipsconn.append(i)#目前这个程序只能查询单一连接符号
                if(tmp==1 and tmpkg==0 and i!=''):
                    searchkeys.append(i)
                if(tmp==2 and tmpkg==0 and i!=''):
                    searchforms.append(i)
                if(tmp==3 and tmpkg==0 and i!=''):
                    searchtips.append(i)
            #再次解析键值
            tmpkeys=[]
            for i in range(len(searchkeys)):
                tmp=re.split(r'[\,]',searchkeys[i])
                for j in tmp:
                    if(j!='or' or j!='and'):
                        tmpkeys.append(j)
            searchkeys=tmpkeys
            #再次解析搜索条件
            tmptips=[]#符号和键和值
            tmptips.append([])#第一位键
            tmptips.append([])#第二位符号
            tmptips.append([])#第三位值
            for i in range(len(searchtips)):
                if(searchtips[i]!='or' or searchtips[i]!='and'):
                    if('>=' in searchtips[i]):
                        tmp=re.split(r'[>=]',re.sub(r'[\"]','',searchtips[i]))
                        tmptips[0].append(tmp[0])
                        tmptips[1].append('>=')
                        tmptips[2].append(tmp[1])
                    elif('<=' in searchtips[i]):
                        tmp=re.split(r'[<=]',re.sub(r'[\"]','',searchtips[i]))
                        tmptips[0].append(tmp[0])
                        tmptips[1].append('<=')
                        tmptips[2].append(tmp[1])
                    elif('>' in searchtips[i]):
                        tmp=re.split(r'[>]',re.sub(r'[\"]','',searchtips[i]))
                        tmptips[0].append(tmp[0])
                        tmptips[1].append('>')
                        tmptips[2].append(tmp[1])
                    elif('<' in searchtips[i]):
                        tmp=re.split(r'[<]',re.sub(r'[\"]','',searchtips[i]))
                        tmptips[0].append(tmp[0])
                        tmptips[1].append('<')
                        tmptips[2].append(tmp[1])
                    elif('=' in searchtips[i]):
                        tmp=re.split(r'[=]',re.sub(r'[\"]','',searchtips[i]))
                        tmptips[0].append(tmp[0])
                        tmptips[1].append('=')
                        tmptips[2].append(tmp[1])
            searchtips=tmptips 
            getkeys=[]
            tmpgetiddata=[]
            alliddata=[]
            for i in searchforms:
                for j in range(len(searchtips[0])):
                    tmpgetiddata.append([])
                    getkeys=self.mycache.saerchKeys(('*_'+i+'_'+searchtips[0][j]+'_*'))
                    if(len(getkeys)!=0):
                        for k in getkeys:
                            tmp=re.split(r'[_+]',k.decode('utf-8'))
                            value=self.mycache.getValue(k.decode('utf-8'))
                            if(searchtips[1][j]=='='):
                                word='"'+value.decode('utf-8')+'"'+searchtips[1][j]+searchtips[1][j]+'"'+searchtips[2][j]+'"'
                            else:
                                word='"'+value.decode('utf-8')+'"'+searchtips[1][j]+'"'+searchtips[2][j]+'"'
                            if(eval(word)):
                                tmpgetiddata[j].append(tmp[0])
                
                #如果一个条件就一个调减连接符len（searchtipsconn）=0
                if(len(searchtipsconn)==0):
                    alliddata=tmpgetiddata
                #如果两个条件就一个调减连接符len（searchtipsconn）=1
                if(len(searchtipsconn)==1):
                    if('and' in searchtipsconn):
                        for j in tmpgetiddata[0]:
                            for k in tmpgetiddata[1]:
                                if(j==k):
                                    alliddata.append(j)
                    if('or' in searchtipsconn):
                        for j in tmpgetiddata[0]:
                            for k in tmpgetiddata[1]:
                                if(k!=j):
                                    alliddata.append(k)
                #如果两个条件以上就一个调减连接符len（searchtipsconn）>1
                if(len(searchtipsconn)>1):
                    for t in range(len(searchtipsconn)):
                        if((searchtipsconn[t]=='and') and (t==0)):
                            for j in tmpgetiddata[0]:
                               for k in tmpgetiddata[1]:
                                  if(j==k):
                                     alliddata.append(j)
                        if((searchtipsconn[t]=='or') and (t==0)):
                            for j in tmpgetiddata[0]:
                               for k in tmpgetiddata[1]:
                                  if(j!=k):
                                     alliddata.append(k)
                        if((searchtipsconn[t]=='and') and (t>0)):
                            tmptmp=[]
                            for j in alliddata:
                               for k in tmpgetiddata[t+1]:
                                  if(k==j):
                                     tmptmp.append(j)
                            alliddata=tmptmp
                        if((searchtipsconn[t]=='or') and (t>0)):
                            for j in alliddata:
                               for k in tmpgetiddata[t+1]:
                                  if(k!=j):
                                     alliddata.append(k)
                if(alliddata[0]):
                    for j in range(len(alliddata)):
                        isalltipsisokvalue=[]
                        for tmpj in range(len(searchkeys)):
                            tmpdata=self.mycache.saerchKeys(alliddata[j]+'_*_'+i+'_'+searchkeys[tmpj]+'_*')
                            value=self.mycache.getValue(tmpdata[0].decode('utf-8'))
                            isalltipsisokvalue.append(value)
                        values.append(isalltipsisokvalue)
            for i in range(len(values)):
                for j in range(len(values[i])):
                    values[i][j]=values[i][j].decode('utf-8')
            if(len(values)==0):
                values=list(self.mydb.getData(words))
            print('原始语句：'+words)
            print('语句拆分结果：'+str(key))
            print('查询结果：'+str(values))
            if(len(values)!=0):
                return values
            else:
                return None
        if(typenum==0):
            values=list(self.mydb.getData(words))
            if(len(values)!=0):
                return values
            else:
                return None
    def insertWord(self,words,typenum):
        if(typenum==0):
            result=self.mydb.insertData(words)
            if(result):
                return True
            else:return False
            
            
if __name__ == "__main__":
     a=myIdc()
     word='SELECT id FROM `members-login` WHERE loginuser="oo28KwWwLRc6lqDewkRz9TSNe8SY"'
     a.searchWord(word,1)

        
    
