# -*- coding:utf-8 -*-
'''
Author: Feng Wenqiang
E-mail: hoontu@sina.com
'''
import pymysql
import redis
import os
import random

class myDb():
    def __init__(self):
        self.dataconfig={}
        self.cacheip=''
        self.cacheport=0
        self.randomnum=5 #随机变量的位数，访问量越多可以设置越多./lib/cache第三行
        self.getSetting()
    def connect(self):
        conn=pymysql.connect(**self.dataconfig)
        return conn
    def randomkey(self):
        key='_'
        for i in range(self.randomnum):
          key=key+random.choice('abcdefghijklmnopqrstuvwxyz')
        key=key+str(random.randint(0,99999))
        return key
    def createCache(self,data):
        pool = redis.ConnectionPool(host=self.cacheip, port=self.cacheport)
        r=redis.Redis(connection_pool=pool)
        pipe = r.pipeline(transaction=True)
        r.mset(data)
        pipe.execute()
    def getSetting(self):
        #初始化数据库
        fp=open('./lib/database.wenq')
        text=fp.readlines()
        self.dataconfig={
          'host':text[0].strip('\n'),#第一行是ip
          'port':int(text[1].strip('\n')),#第二行是端口
          'user':text[2].strip('\n'),#第三行是用户名
          'password':text[3].strip('\n'),#密码
          'db':text[4].strip('\n'),#数据库名
          'charset':text[5].strip('\n'),#编码
          }
        fp.close()
        #初始化缓存配置
        fp=open('./lib/cache.wenq')
        text=fp.readlines()
        self.cacheip=text[0].strip('\n')#第一行是ip
        self.cacheport=int(text[1].strip('\n'))#第二行是端口
        self.randomnum=int(text[2].strip('\n'))#第三行是随机数位数，越高容错越高
        fp.close()
    def delCache(self,data,typenum):
        #typenum是判断变量，为1是有准确的数，data是字典，为0是删除所有，data就不是字典了，0比较危险，这里不添加了
        if(typenum==1):
            pool = redis.ConnectionPool(host=self.cacheip, port=self.cacheport)
            r=redis.Redis(connection_pool=pool)
            pipe = r.pipeline(transaction=True)
            isexists=1
            for i in data:
                if(not r.exists(i) or r.get(i).decode('utf-8')!=data[i]):
                    isexists=0
            #上面判断是否每个数据都是有的，防止数据不完整，产生碎片
            if(isexists==1):
                newkey=[]
                isrightkey=0
                for key in data:
                    #data是字典，变量名被_分割后的列表，0位是数据库名，1位是表名，2是建名，3为唯一插入识别
                    list_database=key.split('_')#分割缓存名称
                    newkey.append(('*_'+list_database[3]))#得到*_+缓存唯一同批次操作识别码（为唯一插入识别）
                for i in newkey:#利用循环查看是否要删除的为同一批数据，不是则报错，是则删除，isrightkey为判断变量
                    if newkey[0]!=i:isrightkey=1
                if(isrightkey==0):#isrightkey变量为0表示删除的数据正确获取同批次所有缓存数据
                    dellist=r.keys(pattern=newkey[0])
                    #获取同批次所有缓存数据dellist后先删除缓存
                    for i in dellist:
                        r.delete(i)
                    #然后再查询数据库，看是否存在该数据，首先需要循环获得判断语句
                    word=''
                    for key in data:
                        list_database=key.split('_')#分割缓存名称,循环将每个变量都添加条件，防止误删
                        word=word+str(list_database[2])+"="+str(data[key])+' and '
                    word="delete from "+str(list_database[1])+" where "+word[:-5]+";"
                    my_conn=self.connect()
                    try:
                        with my_conn.cursor() as cur:
                            cur.execute(word)
                            my_conn.commit()
                            my_conn.close()
                    except:
                        my_conn.rollback()
                        my_conn.close()
            pipe.execute()
                
    def saveCache(self):
        #同步数据库和缓存
        pool = redis.ConnectionPool(host=self.cacheip, port=self.cacheport)
        r=redis.Redis(connection_pool=pool)
        pipe = r.pipeline(transaction=True)
        data=r.keys(pattern='*')
        tmp=[]
        for key in data:
            list_database=key.decode('utf-8').split('_')
            tmp.append(list_database[3])
        tmp_notsame=list(set(tmp))#出去重复的
        for key in tmp_notsame:
            search='*_'+key
            data=r.keys(pattern=search)
            keys=[]
            values=[]
            word=''
            keyword=''
            valueword=''
            i=0
            for key in data:
                list_database=key.decode('utf-8').split('_')
                keys.append(list_database[2])
                values.append(r.get(key.decode('utf-8')).decode('utf-8'))
            for i in range(len(keys)):
                word=word+ ' '+keys[i]+'='+values[i]+' and '
                keyword=keyword+keys[i]+','
                valueword=valueword+'"'+values[i]+'"'+','
            form=list_database[1]
            databasename=list_database[0]
            if(databasename==self.dataconfig['db']):
                word="select * from "+form+" where "+word+";"
                word=word[:-6]+';'
                keyword=keyword[:-1]
                valueword=valueword[:-1]
                my_conn=self.connect()
                try:
                    with my_conn.cursor() as cur:
                        if(cur.execute(word)):
                            my_conn.commit()
                            my_conn.close()
                        else:
                            word="insert into "+form+' ('+keyword+') '+'VALUES ('+valueword+");"
                            cur.execute(word)
                            
                            my_conn.commit()
                            my_conn.close()
                except:
                    my_conn.rollback()
                    my_conn.close()
                pipe.execute()              
                #print("同步完成")
            #else:print("跳过session等无效数据！")
    def searchCache(self,data,typenum):
    #本函数为重点，查询相关数据，如果缓存中有该数据组，则不访问数据库，无则访问查询语法也是字典｛表：数据｝，typenum是0识别模糊查询用的，暂时补考虑模糊查询，typenum是1精确查询，typenum是2跨表查询
        if(typenum==1):
            newkey=[]
            form=[]
            keys=[]
            isrightkey=0
            for key in data:
                #data是字典，变量名被_分割后的列表，0位是数据库名，1位是表名，2是建名，3为唯一插入识别
                list_database=key.split('_')#分割缓存名称
                newkey.append(('*_'+list_database[2]+'_*'))#得到*_+健名+_*通配数据
                form.append(list_database[1])#得到表名数据
            pool = redis.ConnectionPool(host=self.cacheip, port=self.cacheport)
            r=redis.Redis(connection_pool=pool)
            pipe = r.pipeline(transaction=True)
            newkeys=[]
            for key in newkey:
                newkeys.append(r.keys(pattern=key))
            for i in newkeys:
                #获得唯一识别码
                for key in i:
                    list_database=key.decode('utf-8').split('_')#分割缓存名称
                    keys.append(('*_'+list_database[3]))#得到*_+缓存唯一同批次操作识别码（为唯一插入识别）
            keys=list(set(keys))
            for i in form:#利用循环查看是否要查询的为同一表，不是则报错，是则继续，isrightkey为判断变量
                if form[0]!=i:isrightkey=1
            if(isrightkey==0):#isrightkey变量为0表示是同表数据
                searchlist=[]
                searchvalue=[]
                #循环获得去重后的数据并获得完整的变量
                for i in keys:
                    searchlist.append(r.keys(pattern=i))
                #获取所有缓存中的名称
                for i in searchlist:
                    t=[]
                    for j in i:
                        t.append(r.get(j.decode('utf-8')))
                    searchvalue.append(t)
                pipe.execute()
                keys=[]
                values=[]
                result=[]
                for i in range(len(searchlist)):
                    t=[]
                    q=[]
                    for j in range(len(searchlist[i])):
                        t.append(searchlist[i][j].decode('utf-8'))
                        q.append(searchvalue[i][j].decode('utf-8'))
                    keys.append(t)
                    values.append(q)
                result.append(keys)
                result.append(values)
                return result
                '''#然后再查询数据库，看是否存在该数据，首先需要循环获得判断语句
                word=''
                for key in data:
                    list_database=key.split('_')#分割缓存名称,循环将每个变量都添加条件，防止误删
                    word=word+str(list_database[2])+"="+str(data[key])+' and '
                word="delete from "+str(list_database[1])+" where "+word[:-5]+";"
                print(word)
                my_conn=self.connect()
                try:
                    with my_conn.cursor() as cur:
                        print(cur.execute(word))
                        my_conn.commit()
                        my_conn.close()
                except:
                    my_conn.rollback()
                    my_conn.close()'''
    def getData(self,word):
        key=word
        with self.conn.cursor() as cur:
            cur.execute(key)
            data=cur.fetchall()
        return data
    def insertData(self,word):
        key=word
        try:
            with self.conn.cursor() as cur:
                isok=cur.execute(key)
                self.conn.commit()
            return isok
        except:
            self.conn.rollback()

    def delData(self,word):
        key=word
        try:
            with self.conn.cursor() as cur:
                isok=cur.execute(key)
                self.conn.commit()
            return isok
        except:
            self.conn.rollback()
    def closeData(self):
        self.conn.close()
if __name__ == "__main__":
    oo=myDb()
    word='SELECT * FROM `bankinfor` WHERE 1 '
    n=oo.getData(word)
    print(n)
