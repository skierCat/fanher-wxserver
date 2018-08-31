# -*- coding:utf-8 -*-
'''
Author: Feng Wenqiang
E-mail: hoontu@sina.com
'''
from methods.webcache import myCache
class Wxcache(object):
    """
    微信token缓存
    """
    _expire_access_token = 7200  # 微信access_token过期时间, 2小时
    _expire_js_token = 30 * 24 * 3600   # 微信js网页授权过期时间, 30天
    KEY_ACCESS_TOKEN = 'access_token'  # 微信全局唯一票据access_token
    KEY_JSAPI_TICKET = 'jsapi_ticket'  # JS_SDK权限签名的jsapi_ticket
    def get_cache(self,key):
        cache=myCache()
        return cache.getValue(key)
    def insert_cache(self,key,tmpdata):
        cache=myCache()
        value=cache.getValue(key)
        if(value==''):
            insertdata={}
            insertdata[key]=tmpdata
            cache.createCache(insertdata)
        elif(value!=''):
            cache.updateValue(key,tmpdata)
