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

        pages = 15
        photos = None

        ps = self.db.photos.find().sort("upload_time",pymongo.DESCENDING)  # DESCENDING .ASCENDING
        if page == 1:
            photos = ps[page-1:pages]
        elif page > 1: 
            print (page-1)*pages
            print pages*page
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
        self.render('index.html',photo_list = photo_list)

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
