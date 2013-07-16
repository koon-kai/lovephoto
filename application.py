#!/usr/bin/env python
# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf8")

import os.path
import re

import memcache
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import handler.base
import handler.index
import handler.connect
import handler.user
import handler.photo
import handler.error
import config

from tornado.options import define, options
from tornado.escape import json_decode
from gridfs import GridFS
from database import mongo_client

define("port", default = 5000, help = "run on the given port", type = int)

class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__), "template"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            site_path = config.SITE_PATH,
            thumb_dir = config.THUMB_DIR,
            xsrf_cookies = True,
            cookie_secret = config.SECRET_KEY,
            login_url = "/login",
            autoescape = None,
	        debug = True,
        )

        handlers = [
            (r"/", handler.index.IndexHandler),
            (r"/load", handler.index.IndexHandler),
            (r"/about", handler.index.AboutHandler),
            (r"/get/photo/(\w+)", handler.photo.PhotoHandler),
            (r"/get/thumb_photo/(\w+)", handler.photo.PhotoThumbHandler),
            (r"/get/index_thumb/(\w+)/(\w+)", handler.photo.IndexThumbHandler),
            (r"/show/photo/(\w+)", handler.photo.ShowPhotoHandler),
            (r"/photo/like/(\w+)", handler.photo.PhotoLikeHandler),
            (r"/connect/callback/(.*)", handler.connect.ConnectCallbackHandler),
            (r"/connect/(.*)", handler.connect.ConnectHandler),
            (r"/logout", handler.user.LogoutHandler),
            (r"/login", handler.user.LoginHandler),
            (r"/share", handler.user.ShareHandler),
            (r"/share/photo", handler.user.SharePhotoHandler),
            (r"/share/photo/submit", handler.user.ShareHandler),
            (r"/share/delete/thumb", handler.user.DelThumbHandler),
            (r"/user/photos/(\w+)", handler.user.UserPhotosHandler),
            (r"/del/photo/(\w+)", handler.user.DelPhotoHandler),
            (r"/submit/comment", handler.user.SubmitCommentHandler),
            (r".*", handler.error.PageNotFoundHandler),
        ]

        tornado.web.Application.__init__(self, handlers, **settings)

        # mongodb
        self.db = mongo_client[config.MDB_NAME]
        
        # memcache
        self.mc = memcache.Client(['%s:%s' % (config.MEMCACHED_HOST, config.MEMCACHED_PORT)], debug=0)

        # redis
        #self.cache = redis_conn

        #mongodb gridfs
        self.fs = GridFS(self.db,'photos')
        
        
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    print 'Server starting on 127.0.0.1:%s ...' % options.port
    tornado.ioloop.IOLoop.instance().start()
  

if __name__ == "__main__":
    main()
