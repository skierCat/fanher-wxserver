# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun#osgeo.cn
CopyRight: http://www.yunsuan.org
Bu Kun's Homepage: http://bukun.net
'''

import tornado.web
import os
from url import url
import methods.mconfig
from methods.mconfig import SITE

# 添加扩展的模块。
# from modules.extends import *
class myWeb(tornado.web.Application):
    def __init__(self):
        settings = dict(
            title=SITE,
            template_path=os.path.join(os.path.dirname(__file__), "myhtml"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            cookie_secret=methods.mconfig.cookie_secret,
            debug=True,
        )
        super(myWeb, self).__init__(handlers=url, **settings)
        # Have one global connection to the blog DB across all handlers

if __name__ == '__main__':
    myWeb()
    pass
