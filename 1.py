# -*- coding:utf-8 -*-
'''
Author: Feng Wenqiang
E-mail: hoontu@sina.com
'''
from methods.db import myDb
import random
import time
time1 = time.time()
sdata1={'finance_tmp_id':122}
for i in range(1000):
    intone=random.randint(1,99999999)
    inttwo=random.randint(1,99999999)
    intz=random.randint(1,99999999)
    db=myDb()
    key='finance_tmp_id'
    kez='finan_tmp_id'
    kex='finance_tmp_ip'
    p=db.randomkey()
    q=db.randomkey()
    key=key+p
    kex=kex+p
    kez=kez+q
    deldata1='finance_tmp_id_btgxbtdwdw17720'
    deldata2='finance_tmp_ip_btgxbtdwdw17720'
    dist={key:intone,kex:inttwo,kez:intz}
    dist1={deldata1:'38572953',deldata2:'39246297'}
    db.createCache(dist)

time2 = time.time()
print((time1-time2))
db.saveCache()
time3 = time.time()
print((time3-time2))
db.delCache(dist1,1)
t=db.searchCache(sdata1,1)
for i in range(len(t[0])):
    for j in range(len(t[0][i])):
        print(t[0][i][j])
        print(t[1][i][j])
