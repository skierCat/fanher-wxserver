# -*- coding:utf-8 -*-
'''
Author: Wen
'''

import json
import time
import xlrd
import random
import os
import tornado.web
from methods.webcache import myCache
from methods.webmysql import myDb
from tornado.websocket import WebSocketHandler

class ReceiveexcelHandler(WebSocketHandler):
    #判断字符串是否是时间   
    def is_str_time(self,string):
        try:
            time.strptime(string,"%Y-%m-%d")
            return True
        except:
            return False
    def check_origin(self, origin):
        return True
    def open(self):
        pass

    def on_message(self, getdata):
        #print(type(getdata))
        if(type(getdata)==str):
            data=json.loads(getdata)
            filebyte={}
            if('user' in data):
                cache=myCache()
                key='uploadexcel_'+data['user']+'_'+str(data['size'])
                receivecache={}
                receivecache[key]=''
                cache.createCache(receivecache)
                filebyte['size']=0
                self.write_message(json.dumps(filebyte).encode())
                #print('数据对接成功')
            #保存修改的最终数据
            elif(('date' in data) & ('xmb' in data)):
                #print('开始保存工资信息')
                if(os.path.exists('tmp/stamp.wenq')==False):
                    fp=open('tmp/stamp.wenq','w')
                    fp.write(str(100000000))
                    fp.close()
                if(os.path.exists('tmp/stamp.wenq')):
                    fp=open('tmp/stamp.wenq','r')
                    stamp=fp.read()
                    fp.close()
                    stamp=int(stamp)+1
                    fp=open('tmp/stamp.wenq','w')
                    fp.write(str(stamp))
                    fp.close()
                    stamp=str(time.strftime('%Y%m%d',time.localtime(time.time())))+str(stamp)
                if((data['date']!=None) & (data['xmb']!=None) & (len(data['datainfo'])!=0)):
                    cache=myCache()
                    getdate=data['date'].split('-')
                    xmb=data['xmb']
                    uploader=data['uploader']
                    redishead=cache.dataconfig['db']+'_'+'members-wages'+'_'
                    for item in data['datainfo']:
                        numrandom=cache.randomkey()
                        wages=str(item)
                        redisset={}
                        redisdata=numrandom+'_'+redishead+'batch'+'_'+item['姓名']+'_1'
                        redisset[redisdata]=stamp
                        redisdata=numrandom+'_'+redishead+'name'+'_'+item['姓名']+'_1'
                        redisset[redisdata]=item['姓名']
                        redisdata=numrandom+'_'+redishead+'year'+'_'+item['姓名']+'_1'
                        redisset[redisdata]=getdate[0]
                        redisdata=numrandom+'_'+redishead+'month'+'_'+item['姓名']+'_1'
                        redisset[redisdata]=getdate[1]
                        redisdata=numrandom+'_'+redishead+'uploader'+'_'+item['姓名']+'_1'
                        redisset[redisdata]=uploader
                        redisdata=numrandom+'_'+redishead+'wages'+'_'+item['姓名']+'_1'
                        redisset[redisdata]=wages
                        redisdata=numrandom+'_'+redishead+'userlimit'+'_'+item['姓名']+'_1'
                        redisset[redisdata]=data['xmb']
                        cache.createCache(redisset)
                    self.write_message(json.dumps({'log':'上传成功！'}).encode())              
        elif(type(getdata)==bytes):
            filename=str(time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())))+str(random.randint(10000,99999))+'.xls'
            url='tmp/'+filename
            #print(url)
            fp=open(url,'wb')
            fp.write(getdata)
            fp.close()
            getdisc=self.fenxiexcel(url)
            self.write_message(json.dumps(getdisc).encode())
    def on_close(self):
        pass
    def fenxiexcel(self,file):
        #print('开始分析工资表')
        myexcel=xlrd.open_workbook(file)
        title=[]
        data=[]
        infor=''
        gzformfx=[]
        dicdata={}
        #获得最全标题
        for i in range(myexcel.nsheets):
            table=myexcel.sheet_by_index(i)
            title.append([])
            for j in range(table.nrows-1):
                tmpnum=0
                tmp=''
                t=table.row_values(j)
                p=table.row_values(j+1)
                noblank=[]
                noblank_title=[]
                for k in range(len(t)):
                    if(isinstance(t[k],float)==True):
                        t[k]=''.join(str(t[k]).split())
                    if(isinstance(t[k],int)==True):
                        t[k]=''.join(str(t[k]).split())
                    if(isinstance(t[k],str)==True):
                        t[k]=''.join(t[k].split())
                for k in range(len(p)):
                    if(isinstance(p[k],float)==True):
                        p[k]=''.join(str(p[k]).split())
                    if(isinstance(p[k],int)==True):
                        p[k]=''.join(str(p[k]).split())
                    if(isinstance(p[k],str)==True):
                        p[k]=''.join(p[k].split())
                for k in range(len(t)-1):
                    if(k>=2):
                        if(t[k-1]!='' and t[k]=='' and p[k]!=''):
                            t[k-1]=p[k-1]
                for k in range(len(t)-1):
                    if(k>=2):
                        if(t[k]=='' and p[k]!=''):
                            t[k]=p[k]
                if(len(t)>=len(title[i])):
                    tipnum=0
                    for tip in t:
                        if(tip=='姓名'):
                            tipnum=1
                        if(tipnum==1):
                            infor='得到标题！'
                            title[i]=t
                        else:
                            infor='表格错误！'
                    else:
                        infor='表格为空！'
        for i in range(myexcel.nsheets):
            table=myexcel.sheet_by_index(i)
            for j in range(table.nrows):
                tmpnum=0
                t=table.row_values(j)
                theme=title[i]
                noblank=[]
                data.append([])
                for k in range(len(t)):
                    if(isinstance(t[k],float)==True):
                        t[k]=''.join(str(t[k]).split())
                    if(isinstance(t[k],int)==True):
                        t[k]=''.join(str(t[k]).split())
                    if(isinstance(t[k],str)==True):
                        t[k]=''.join(t[k].split())
                    if(t[k]!=''):
                        noblank.append(t[k])
                for k in range(len(theme)):
                    if(theme[k]=='姓名'):
                        if(t[k]!='' and len(noblank)>3 and t[k]!='姓名' and t[k]!='管理人员' and t[k]!='见习生' and t[k]!='工程部' and t[k]!='小计'  and t[k]!='合计'):
                            tmpnum=1
                if(tmpnum==1):
                    tmptext=''
                    tmpname=''
                    dicdatatmp={}
                    dicdatatmp.clear()
                    if(os.path.exists('tmp/stamp.wenq')==False):
                        fp=open('tmp/stamp.wenq','w')
                        fp.write(str(100000000))
                        fp.close()
                    if(os.path.exists('tmp/stamp.wenq')):
                        fp=open('tmp/stamp.wenq','r')
                        stamp=fp.read()
                        fp.close()
                        stamp=int(stamp)+1
                        fp=open('tmp/stamp.wenq','w')
                        fp.write(str(stamp))
                        fp.close()
                    stamp=str(time.strftime('%Y%m%d',time.localtime(time.time())))+str(stamp)
                        #扩展分析工资表格的表单
                    gzformfx.append([])
                    gzformfx[len(gzformfx)-1].append(stamp)
                    for k in range(len(t)):
                        tips_getblanknum=0
                        for tipsj in range(8):
                            if(k>8):
                                if(t[k-tipsj]==''):
                                    tips_getblanknum=tips_getblanknum+1
                        if(tips_getblanknum==9):
                            break
                            #gzformfx中空格的处理必须加上
                        if(t[k]==''):
                            #抽出需要列入数据库的数据
                            if(theme[k]=='姓名' and (t[k] not in gzformfx)):
                                if(len(t[k])>10):
                                    gzformfx[len(gzformfx)-1].append(t[k][:10])
                                else:gzformfx[len(gzformfx)-1].append(t[k])
                            if(theme[k]=='应付工资及奖金'):
                                if(len(t[k])>10):
                                    gzformfx[len(gzformfx)-1].append(t[k][:10])
                                else:gzformfx[len(gzformfx)-1].append(t[k])
                            if(theme[k]=='实付工资' and (t[k] not in gzformfx)):
                                if(len(t[k])>10):
                                    gzformfx[len(gzformfx)-1].append(t[k][:10])
                                else:gzformfx[len(gzformfx)-1].append(t[k])
                            if(theme[k]=='各类补贴\奖金' and (t[k] not in gzformfx)):
                                if(len(t[k])>10):
                                    gzformfx[len(gzformfx)-1].append(t[k][:10])
                                else:gzformfx[len(gzformfx)-1].append(t[k])
                            if(theme[k]=='公积金' and (t[k] not in gzformfx)):
                                gzformfx[len(gzformfx)-1].append(t[k])
                            if(theme[k]=='养老金' and (t[k] not in gzformfx)):
                                gzformfx[len(gzformfx)-1].append(t[k])
                            if(theme[k]=='待业金' and (t[k] not in gzformfx)):
                                gzformfx[len(gzformfx)-1].append(t[k])
                            if(theme[k]=='医保' and (t[k] not in gzformfx)):
                                gzformfx[len(gzformfx)-1].append(t[k])
                            if(theme[k]=='个人所得税' and (t[k] not in gzformfx)):
                                gzformfx[len(gzformfx)-1].append(t[k])
                        if(t[k]!='' and theme[k]!='序号' and theme[k]!='签章'):
                            tmptext=tmptext+theme[k]+' ： '+t[k]+'\n'
                            #抽出需要列入数据库的数据
                            if(theme[k]=='姓名' and (t[k] not in gzformfx)):
                                gzformfx[len(gzformfx)-1].append(t[k])
                            if(theme[k]=='应付工资及奖金' and (t[k] not in gzformfx)):
                                gzformfx[len(gzformfx)-1].append(t[k])
                            if(theme[k]=='各类补贴\奖金' and (t[k] not in gzformfx)):
                                gzformfx[len(gzformfx)-1].append(t[k])
                            if(theme[k]=='公积金' and (t[k] not in gzformfx)):
                                gzformfx[len(gzformfx)-1].append(t[k])
                            if(theme[k]=='养老金' and (t[k] not in gzformfx)):
                                gzformfx[len(gzformfx)-1].append(t[k])
                            if(theme[k]=='待业金' and (t[k] not in gzformfx)):
                                gzformfx[len(gzformfx)-1].append(t[k])
                            if(theme[k]=='医保' and (t[k] not in gzformfx)):
                                gzformfx[len(gzformfx)-1].append(t[k])
                            if(theme[k]=='个人所得税' and (t[k] not in gzformfx)):
                                gzformfx[len(gzformfx)-1].append(t[k])
                            if(theme[k]=='实付工资' and (t[k] not in gzformfx)):
                                if(len(t[k])>10):
                                    gzformfx[len(gzformfx)-1].append(t[k][:10])
                                else:gzformfx[len(gzformfx)-1].append(t[k])
                            if(theme[k]=='签章'):
                                tmptext=tmptext+theme[k]+' ： '+stamp+'\n'
                        if(theme[k]!='序号' and theme[k]!='签章'):
                            dicdatatmp[theme[k]]=t[k]
                        if(t[k]!='' and theme[k]=='姓名'):
                            tmpname=t[k]
                    data[i].append(stamp)
                    data[i].append(tmpname)
                    data[i].append(tmptext)
                    dicdata[str(stamp)]=dicdatatmp
        else:
            send_data={'text':'上传失败！'}
        tmpstamp=[]
        tmpnames=[]
        tmptexts=[]
        text='' 
        return(dicdata)
        

        

