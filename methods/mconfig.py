# -*- coding:utf-8 -*-
'''
Author: Feng Wenqiang
E-mail: hoontu@sina.com
'''
import socket


def hostname():
    return (socket.gethostname())

page_num = 2

SITE = r'文强原始凭证查询系统'
SITEURL = hostname()
PORT = 8001
cookie_secret = '123456789abcdef'
torlite_template_name = 'torlite_template'
