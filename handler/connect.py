#!/usr/bin/env python
# coding=utf-8

import datetime
import tornado.web
from tornado.escape import json_decode,json_encode

import base
import config
from api.douban import Douban
from api.sina import SinaWeibo
from api.error import OAuthError
from utils.logger import logging

log = logging.getLogger(__name__)

class ConnectHandler(base.BaseHandler):
    
    def get(self,provider):
        print provider 
        client = None
        if provider == config.OPENID_DOUBAN:
            client = Douban()
        elif provider == config.OPENID_SINA:
            client = SinaWeibo()

        if not client:
            log.warning(u'不合法的路径连接')
            raise tornado.web.HTTPError(400,u"不支持该第三方账户登录")

        try:
            login_uri = client.login()
        except OAuthError,e:
            log.warning(e)
            raise tornado.web.HTTPError(400,u"跳转到第三方失败，请重新尝试一下")

        self.redirect(login_uri)


class ConnectCallbackHandler(base.BaseHandler):
    
    def get(self,provider):
        
        code = self.get_argument("code")

        client = None
        user = None

        openid_type = config.OPENID_TYPE_DICT.get(provider)

        if not openid_type:
            raise tornado.web.HTTPError(404,"not support such provider")

        if provider in [config.OPENID_DOUBAN,config.OPENID_SINA,]:
            if provider == config.OPENID_DOUBAN:
                client = Douban()
            elif provider == config.OPENID_SINA:
                client = SinaWeibo()

            ## oauth2方式授权处理
            try:
                token_dict = client.get_access_token(code)
                log.info(token_dict)
                #print "---token_dict:",token_dict
            except OAuthError,e:
                log.warning(e)
                raise tornado.web.HTTPError(400,u"从第三方获取access_token失败了，请重新尝试一下。")

            if not (token_dict and token_dict.get("access_token")):
                raise tornado.web.HTTPError(400,"no_access_token")

            try:
                access_token = token_dict.get("access_token","")
                refresh_token = token_dict.get("refresh_token","")


                uid = token_dict.get("uid") or token_dict.get("user", {}).get("uid") \
                    or token_dict.get("user", {}).get("id")
                client.set_token(access_token, refresh_token)
                user_info = client.get_user_info(uid)
                log.info(user_info)
                log.info(user_info.data)
            except OAuthError, e:
                log.warning(e)
                raise tornado.web.HTTPError(400, e.msg)

            user = self.save_user_and_token(token_dict, user_info, openid_type)

        if user:
            self.redirect("/")
        else:
            info  = u"连接到"+provider+"失败了，可能是对方网站忙，请稍等重试..."
            log.warning(info)
            raise tornado.web.HTTPError(400,info)


    ## 保存用户信息到数据库，并保存token
    def save_user_and_token(self,token_dict,user_info, openid_type):
        first_connect = False
        u = self.db.user.find_one({"openid_type":openid_type,"user_id":user_info.get_user_id()}) 
        if not u:
            first_connect = True
            user = {
                "openid_type":openid_type,
                "user_id":user_info.get_user_id(),
                "uid": user_info.get_uid(), 
                "name": user_info.get_nickname(), 
                "intro": user_info.get_intro(),
                "signature": user_info.get_signature(),
                "avatar": user_info.get_avatar(),
                "icon": user_info.get_icon(),
                "email": user_info.get_email(),
            }
            self.db.user.insert(user)
    
        ##保存access token (访问记录)
        self.db.login_info.insert({"uid":user_info.get_user_id(),
                                     "access_token":token_dict.get("access_token"),
                                     "token_dict":token_dict.get("refresh_token", ""),
                                     "login_time":datetime.datetime.now(),
                                     "first_connect": "Y" if first_connect else "N",
                                    })
        ##set cookie，保持登录状态
        if not self.get_current_user():
            current_user = {"uid":user_info.get_user_id(),"nickname":user_info.get_nickname(),"avatar":user_info.get_avatar()} 
            self.currentUserSet(current_user)
        return current_user

  




