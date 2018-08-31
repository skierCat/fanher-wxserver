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

import sys     # utf-8，兼容汉字
from bin.index import HomeHandler    #首页
from bin.login import LoginHandler    #登录页面
from bin.admin.managertool.receiveexcel import ReceiveexcelHandler#获得传来的excel
from bin.admin.sysset.limit import LimitsetHandler#系统设置项目部
from bin.admin.admin import AdminHandler    #后台首页
from bin.wxxfh import WxxfhHandler    #微信接口

url = [
    (r"/", HomeHandler),
    (r"/login", LoginHandler),
    (r"/admin", AdminHandler),
    (r"/managertool/receiveexcel", ReceiveexcelHandler),
    (r"/sysset/limit", LimitsetHandler),
    (r"/wxxfh", WxxfhHandler),
]
