# -*- coding:utf-8 -*-
'''
Author: Feng Wenqiang
E-mail: hoontu@sina.com
'''
import tornado.ioloop
import requests
import json
from methods.wxxfhconfig import WxConfig
from methods.wxxfhcache import Wxcache


class WxShedule(object):
    """
    定时任务调度器

    excute                      执行定时器任务
    get_access_token            获取微信全局唯一票据access_token
    get_jsapi_ticket           获取JS_SDK权限签名的jsapi_ticket
    """
    _wx_cache=Wxcache()
    _expire_time_access_token = 7000 * 1000  # token过期时间
    """
    微信token缓存

    set_cache               添加redis
    get_cache               获取redis
    """

    def excute(self):
        """执行定时器任务"""
        print('【获取微信全局唯一票据access_token】>>>执行定时器任务')
        tornado.ioloop.IOLoop.instance().call_later(0, self.get_access_token)
        tornado.ioloop.PeriodicCallback(self.get_access_token, self._expire_time_access_token).start()
        # tornado.ioloop.IOLoop.current().start()

    def get_access_token(self):
        """获取微信全局唯一票据access_token"""
        url = WxConfig.config_get_access_token_url
        r = requests.get(url)
        print('【获取微信全局唯一票据access_token】Response[' + str(r.status_code) + ']')
        if r.status_code == 200:
            res = r.text
            print('【获取微信全局唯一票据access_token】>>>' + res)
            d = json.loads(res)
            if 'access_token' in d.keys():
                access_token = d['access_token']
                # 添加至mysql
                self._wx_cache.insert_cache(self._wx_cache.KEY_ACCESS_TOKEN, access_token)
                # 获取JS_SDK权限签名的jsapi_ticket
                self.get_jsapi_ticket()
                return access_token
            elif 'errcode' in d.keys():
                errcode = d['errcode']
                print(
                    '【获取微信全局唯一票据access_token-SDK】errcode[' + errcode + '] , will retry get_access_token() method after 10s')
                tornado.ioloop.IOLoop.instance().call_later(10, self.get_access_token)
        else:
            print('【获取微信全局唯一票据access_token】request access_token error, will retry get_access_token() method after 10s')
            tornado.ioloop.IOLoop.instance().call_later(10, str(self.get_access_token))

    def get_jsapi_ticket(self):
        """获取JS_SDK权限签名的jsapi_ticket"""
        access_token = (self._wx_cache.get_cache(self._wx_cache.KEY_ACCESS_TOKEN)).decode('utf-8')
        if access_token:
            url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi' % access_token
            r = requests.get(url)
            print('【微信JS-SDK】获取JS_SDK权限签名的jsapi_ticket的Response[' + str(r.status_code) + ']')
            if r.status_code == 200:
                res = r.text
                print('【微信JS-SDK】获取JS_SDK权限签名的jsapi_ticket>>>>' + res)
                d = json.loads(res)
                errcode = d['errcode']
                if errcode == 0:
                    jsapi_ticket = d['ticket']
                    # 添加至mysql中
                    self._wx_cache.insert_cache(self._wx_cache.KEY_JSAPI_TICKET,jsapi_ticket)
                else:
                    print('【微信JS-SDK】获取JS_SDK权限签名的jsapi_ticket>>>>errcode[' + errcode + ']')
                    print('【微信JS-SDK】request jsapi_ticket error, will retry get_jsapi_ticket() method after 10s')
                    tornado.ioloop.IOLoop.instance().call_later(10, self.get_jsapi_ticket)
            else:
                print('【微信JS-SDK】request jsapi_ticket error, will retry get_jsapi_ticket() method after 10s')
                tornado.ioloop.IOLoop.instance().call_later(10, self.get_jsapi_ticket)
        else:
            print('【微信JS-SDK】获取JS_SDK权限签名的jsapi_ticket时,access_token获取失败, will retry get_access_token() method after 10s')
            tornado.ioloop.IOLoop.instance().call_later(10, self.get_access_token)

if __name__ == '__main__':

    wx_shedule = WxShedule()
    """执行定时器"""
    wx_shedule.excute()
