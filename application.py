#!/usr/bin/env python
# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf8")

import os.path
import re

import torndb
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import handler.base
import handler.index
import handler.connect
import handler.user
import handler.photo
import config

from tornado.options import define, options
from tornado.escape import json_decode
from gridfs import GridFS
from utils.logger import logging
from database import mongo_client,redis_conn

define("port", default = 5000, help = "run on the given port", type = int)
#define("mysql_host", default = "127.0.0.1", help = "community database host")
#define("mysql_database", default = "lovelife", help = "community database name")
#define("mysql_user", default = "root", help = "community database user")
#define("mysql_password", default = "root", help = "community database password")

class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__), "template"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            site_path = config.SITE_PATH,
            thumb_dir = config.THUMB_DIR,
            xsrf_cookies = True,
            cookie_secret = "cookie_secret_code",
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
            (r"/submit/comment", handler.user.SubmitCommentHandler),
        ]

        tornado.web.Application.__init__(self, handlers, **settings)

        # Have one global connection to the blog DB across all handlers
        self.db = mongo_client[config.MDB_NAME]
        #self.mc = memcache.Client(['%s:%s' % (config.MEMCACHED_HOST, config.MEMCACHED_PORT)], debug=0)
        self.cache = redis_conn
        #mongodb gridfs
        self.fs = GridFS(self.db,'photos')
        
        self.log = logging.getLogger(__file__)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    print 'Server starting on 127.0.0.1:5000 ...'
    tornado.ioloop.IOLoop.instance().start()
  

if __name__ == "__main__":
    main()
