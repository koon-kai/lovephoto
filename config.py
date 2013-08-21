#!/usr/bin/env python 
# coding:utf-8

import os.path


#-- application config --
SECRET_KEY = 'efku62xkQ02svYusgU3gyUUAEjqvHUWqjowRRlI3Odw='
SITE_COOKIE = 'tsLochevTHaYN2FAmPodz0jcvHc1cEzOmr3JW+stpBI='

SITE_PATH = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = os.path.join(SITE_PATH, 'static')
TEMPLATE_PATH = os.path.join(SITE_PATH, 'template')
LOG_PATH = os.path.join(SITE_PATH,'log')

#-- upload photo dir --
UPLOAD_PHOTO_DIR = STATIC_PATH+'/upload/thumb/'
THUMB_DIR = '/static/upload/thumb/'

#--Mysql db config --
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWD = 'root'
DB_NAME = 'lovelife'


#-- mongodb config --
MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MDB_NAME = 'lovephoto'


#-- redis config --
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0

#-- mc config --
# mc replace redis
MEMCACHED_HOST = "127.0.0.1"
MEMCACHED_PORT = 11211

#-- openid type config --
OPENID_DOUBAN = 'douban'
OPENID_SINA = 'sina'

OPENID_TYPE_DICT = {
    OPENID_DOUBAN : "D",
    OPENID_SINA: "S",
}


#-- oauth key & secret config --
APIKEY_DICT = {
    OPENID_DOUBAN : {
        "key" : "0b26186a93e338912172493fbba9a9b3",
        "secret" : "c26506c3443d1bd8",
        "redirect_uri" : "http://lovephoto.koonkai.me/connect/callback/douban",
    },
    OPENID_SINA : {
        "key" : "2028891700",
        "secret" : "dfe685941eebc04651c4af4533a973f9",
        "redirect_uri" : "http://lovephoto.koonkai.me/connect/callback/sina",
    },
}
