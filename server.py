# -*- coding:utf-8 -*-
'''
Author: Feng Wenqiang
E-mail: hoontu@sina.com
'''
import sys
import tornado.autoreload
import tornado.ioloop
import tornado.locale
import tornado.httpserver
from methods.mconfig import PORT
from methods.wxtokenget import WxShedule
from application import myWeb

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(myWeb())
    if len(sys.argv) > 1:
        print(sys.argv)
        http_server.listen( sys.argv[1] )
    else:
        print(PORT)
        http_server.listen(PORT)
    print('服务器已启动http://127.0.0.1:{0}/'.format(PORT))
    wx_shedule=WxShedule()
    wx_shedule.excute()
    tornado.ioloop.IOLoop.instance().start()
