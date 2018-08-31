# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun#osgeo.cn
CopyRight: http://www.yunsuan.org
Bu Kun's Homepage: http://bukun.net
'''
"""
the url structure of website
"""
import hashlib
import os
import random
import time

import tornado.web

from methods.webmysql import myDb
import numpy as np


class HomeHandler(tornado.web.RequestHandler):
    #判断字符串是否是时间   
    def is_str_time(self,string):
        try:
            time.strptime(string,"%Y-%m-%d")
            return True
        except:
            return False
    def get(self):
        self.render('index.html')
    

            

