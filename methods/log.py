# -*- coding:utf-8 -*-
'''
Author: Feng Wenqiang
E-mail: hoontu@sina.com
'''
import os
import time
class logRobot():
    #日志系统
    def __init__(self,text):
        date=str(int(time.strftime('%Y%m%d%H%M%S  ',time.localtime(time.time()))))
        filename='tmp/log.wenq'
        if(os.path.exists(filename)):
            fp=open(filename,'a')
            log=date+text+'\n'
            fp.write(log)
            fp.close()

