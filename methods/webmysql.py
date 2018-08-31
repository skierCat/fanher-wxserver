# -*- coding:utf-8 -*-
'''
Author: Feng Wenqiang
E-mail: hoontu@sina.com
'''
import pymysql
import os
import zipfile
import traceback

class myDb():
    def __init__(self):
        
        self.dataconfig={}
        self.getSetting()
        
    def getSetting(self):
        #初始化数据库
        fp=open('./lib/database.wenq')
        text=fp.readlines()
        self.dataconfig={
          'host':text[0].strip('\n'),
          'port':int(text[1].strip('\n')),
          'user':text[2].strip('\n'),
          'password':text[3].strip('\n'),
          'db':text[4].strip('\n'),
          'charset':text[5].strip('\n'),
          }
        fp.close()
    def connectSql(self):
        #print(self.dataconfig)
        db=pymysql.connect(**self.dataconfig)
        #print(self.dataconfig)
        return db
        
    def getData(self,word):
        key=word
        #print('连接数据库')
        #print(self.dataconfig)
        conn=self.connectSql()
        #print('连接数据库')
        cur=conn.cursor()
        #print('连接数据库')
        try:
            cur.execute(key)
            #print(key)
            data=cur.fetchall()
            #print(data)
            #print('连接数据库')
        except Exception:
            #print("发生异常",Exception)
            traceback.print_exc()
            conn.rollback()
        finally:
            conn.close()
        return data
    
    def insertData(self,word):
        key=word
        conn=self.connectSql()
        cur=conn.cursor()
        try:
            #print('开始插入数据')
            result=cur.execute(key)
            conn.commit()
        except Exception:
            #print("发生异常",Exception)
            traceback.print_exc()
            self.conn.rollback()
        finally:
            conn.close()
        return result
    
    def delData(self,word):
        key=word
        conn=self.connectSql()
        cur=conn.cursor()
        try:
            cur.execute(key)
            conn.commit()
        except:
            conn.rollback()
        finally:
            conn.close()
if __name__ == "__main__":
    oo=myDb()
    word='SELECT * FROM `bankinfor` WHERE 1 '
    n=oo.getData(word)
    #print(n)
