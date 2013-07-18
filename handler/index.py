#!/usr/bin/env python
# coding=utf-8

import base
import pymongo


class IndexHandler(base.BaseHandler):
    def get(self):

        page = self.get_argument('page',None)
        if not page:
            page = 1
        else:
            page = int(page)

        pages = 10
        photos = None
        photo_count = None
        
        photo_count = self.mc.get('photo_count')
        if not photo_count:
            photo_count = self.db.photos.find().count()
            self.mc.set("photo_count",photo_count)

        ps = self.db.photos.find().sort("upload_time",pymongo.DESCENDING)
        if page == 1:
            photos = ps[page-1:pages]
        elif page > 1: 
            photos = ps[(page-1)*pages:pages*page]

        photo_list = []
        photo_info = {}
        for p in photos:
            photo_info = {
                "id" : p['_id'],
                "uid" : p['uid'],
                "pid" : p['pid'],
                "desc" : p['desc'],
                "height" :(lambda x,y:int((float(y)/float(x))*260))(p['width'],p['height']),
                "comment_num" : p['comment_num'],
                "like" : p['like'],
                'user_avatar' : self.get_avatar_by_uid(p['uid']),
                'user_name' : self.get_username_by_uid(p['uid']),
                }
            photo_list.append(photo_info)
        self.render('index.html',photo_list = photo_list,photo_count=photo_count)

    def get_avatar_by_uid(self,uid):
        user = self.db.user.find_one({"user_id":uid})
        if not user:
            return None
        return user['avatar']

    def get_username_by_uid(self,uid):
        user = self.db.user.find_one({"user_id":uid})
        if not user:
            return None
        return user['name']


class AboutHandler(base.BaseHandler):
    def get(self):
        self.render("about.html")
