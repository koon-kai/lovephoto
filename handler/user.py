#!/usr/bin/env python
# coding=utf-8

import os
import StringIO
import bson
import Image
import tornado
import base
import datetime
import pymongo
from tornado.escape import json_decode,json_encode
from utils.img_tools import make_thumb,del_thumb
from utils.logger import logging

log = logging.getLogger(__name__)

#提交照片
class ShareHandler(base.BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render('share.html')

    @tornado.web.authenticated
    def post(self):
        img = self.request.files['uploadImg'][0]
        photo_desc = self.get_argument('photo_desc')
        thumb_dir = self.get_argument('node_Img')
        pid = self.fs.put(img['body'])
        img_size = Image.open(StringIO.StringIO(img['body'])).getbbox()
        user =json_decode(self.get_current_user())
        photo = {
           "uid":user['uid'],
           'pid':pid,
           'desc':photo_desc,
           'width':img_size[2],
           'height':img_size[3],
           'comment_num':0,
           'like':0,
           'upload_time':datetime.datetime.now()
        }
        self.db.photos.insert(photo)

        file_dir = self.site_path + thumb_dir 
        try:
            del_thumb(file_dir)
        except Exception,e:
            log.error(e)
            raise tornado.web.HTTPError(404,e)

        self.mc.delete('photo_count')
        self.redirect('/user/photos/'+user['uid'])


#上传照片
class SharePhotoHandler(base.BaseHandler):

    @tornado.web.authenticated
    def post(self):
        info = None
        thumb_dir = None
        try:
            photos = self.get_request_files('uploadImg')
            for p in photos:
                sio_photo = StringIO.StringIO(p['body'])
                photo_name = make_thumb(sio_photo)
                sio_photo.close()

            thumb_dir = str(self.thumb_dir) + photo_name
        except AssertionError,e:
            info = u'只能上传图片格式的文件！'
            log.info(info)
        #photos = self.request.files['uploadImg']

        data = {"info":info,"dir":thumb_dir}
        self.write(json_encode(data))


class UserPhotosHandler(base.BaseHandler):

    def get(self,uid):
        user = self.db.user.find_one({"user_id":uid })
        if not user:
            raise tornado.web.HTTPError(404)
        ps = self.db.photos.find({"uid":uid}).sort('upload_time',pymongo.DESCENDING)
        pi = {"user":user,"ps":ps}
        self.render('user_photos.html',pi = pi)


class DelPhotoHandler(base.BaseHandler):

    @tornado.web.authenticated
    def get(self,p_id):
        photo = self.db.photos.find_one({"_id":bson.objectid.ObjectId(p_id)})
        if not photo:
            raise tornado.web.HTTPError(404)

        pid = photo['pid']
        self.db.photos.remove({"_id":bson.objectid.ObjectId(p_id)})
        self.db.comment.remove({"p_id":p_id})
        self.fs.delete(pid)
        self.mc.delete("index_"+str(pid))
        self.mc.delete("thumb_"+str(pid))
        self.mc.delete("big_"+str(pid))
        self.mc.delete("photo_count")
        user = self.get_current_user()
        self.redirect('/user/photos/'+json_decode(user)['uid'])

#删除缩略图
class DelThumbHandler(base.BaseHandler):

    @tornado.web.authenticated
    def post(self):
        thumb_dir = self.get_argument('thumb_dir')
        file_dir = self.site_path + thumb_dir 
        try:
            del_thumb(file_dir)
        except Exception,e:
            raise tornado.web.HTTPError(404,e)

        self.write('s')


class SubmitCommentHandler(base.BaseHandler):

    @tornado.web.authenticated
    def post(self):
        p_id = self.get_argument('p_id')
        content = self.get_argument('content')
        
        user = self.get_current_user()
        if not user:
            self.redirect('/login')

        comment = {
            "p_id" : p_id,
            "uid" : json_decode(user)['uid'],
            "content" : content,
            "submit_time":datetime.datetime.now(),
        }
        self.db.comment.insert(comment)

        p = self.db.photos.find_one({"_id":bson.objectid.ObjectId(p_id)})
        comment_num = int(p['comment_num'])
        comment_num = comment_num + 1
        self.db.photos.update({"_id":bson.objectid.ObjectId(p_id)},{"$set":{"comment_num":comment_num}})

        self.write("0")
        


#登录
class LoginHandler(base.BaseHandler):

    def get(self):
        self.render('login.html')


#退出
class LogoutHandler(base.BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.clear_cookie('user')
        self.redirect('/')

