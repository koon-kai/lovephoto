#!/usr/bin/env python
# coding=utf-8

import bson 
import Image
import StringIO
import base
import tornado
from tornado.escape import json_encode
from PIL.ExifTags import TAGS
from PIL.PngImagePlugin import PngImageFile
from utils.img_tools import get_thumb
from utils.logger import logging

log = logging.getLogger(__name__)

class PhotoHandler(base.BaseHandler):

    def get(self, pid):
        photo = None
        if not pid:
            raise tornado.web.HTTPError(404)
       
        #photo = self.cache.get('big_'+pid)
        photo = self.mc.get(str('big_'+pid))
        if not photo:
            pfs = self.fs.get(bson.objectid.ObjectId(pid))
            if not pfs:
                raise tornado.web.HTTPError(404)
            photo = pfs.read()
            #self.cache.set('big_'+pid,photo)
            self.mc.set(str('big_'+pid),photo)
        self.write(photo)


class PhotoThumbHandler(base.BaseHandler):

    def get(self, pid):
        photo = None
        if not pid:
            raise tornado.web.HTTPError(404)

        #photo = self.cache.get('thumb_'+pid)
        photo = self.mc.get(str('thumb_'+pid))
        if not photo:
            pfs = self.fs.get(bson.objectid.ObjectId(pid))
            if not pfs:
                raise tornado.web.HTTPError(404)
            photo = pfs.read()
            #self.cache.set('thumb_'+pid,photo)
            self.mc.set(str('thumb_'+pid),photo)

        sio = StringIO.StringIO(photo)
        photo_data = get_thumb(sio)
        sio.close()
        self.write(photo_data)


class IndexThumbHandler(base.BaseHandler):

    def get(self,height,pid):
        photo = None
        if not pid:
            raise tornado.web.HTTPError(404)

        #photo = self.cache.get('index_'+pid)
        photo = self.mc.get(str('index_'+pid))
        if not photo:
            pfs = self.fs.get(bson.objectid.ObjectId(pid))
            if not pfs:
                raise tornado.web.HTTPError(404)
            photo = pfs.read()
            #self.cache.set('index_'+pid,photo)
            self.mc.set(str('index_'+pid),photo)

        sio = StringIO.StringIO(photo)
        photo_data = get_thumb(sio,260,int(height))
        sio.close()
        self.write(photo_data)


class PhotoLikeHandler(base.BaseHandler):

    def get(self,pid):
        photo = self.db.photos.find_one({'_id':bson.objectid.ObjectId(pid)})
        if not photo:
            raise tornado.web.HTTPError(404)
        like = int(photo['like'])
        like = like + 1
        self.db.photos.update({"_id":bson.objectid.ObjectId(pid)},{"$set":{"like":like}})
        data = {"isOk":"true","message":pid}
        self.write(json_encode(data))


class ShowPhotoHandler(base.BaseHandler):

    def get(self,pid):
        photo = self.db.photos.find_one({'_id':bson.objectid.ObjectId(pid)})
        if not photo:
            raise tornado.web.HTTPError(404)

        user = self.db.user.find_one({'user_id':photo['uid']})

        p = self.fs.get(bson.objectid.ObjectId(photo['pid']))
        exif_info = self.get_exif_info(p)
        photo_info = {
            "id":pid,
            "pid":photo['pid'],
            "uid":user['user_id'],
            "desc":photo['desc'],
            "user_name" : user['name'],
            "user_avatar" : user['avatar'],
            "upload_time" : photo['upload_time'],
        }
        if exif_info:
            try:
                photo_info["has_exif"] = "true"
                photo_info["camera_brand"] =  exif_info['Make']  #相机品牌
                photo_info["camera_model"] = exif_info['Model']  #相机型号
                photo_info["date_taken"] = exif_info.has_key('DateTime') and exif_info['DateTime'] or exif_info['DateTimeOriginal']  #拍摄时间
                photo_info["exposure_time"] = (lambda x:str(x[0])+'/'+str(x[1]))(exif_info['ExposureTime']) #曝光时间
                photo_info["aperture_value"] = (lambda x:float('%0.2f'%(float(x[0])/float(x[1]))))(exif_info['ApertureValue']) #光圈大小
                photo_info["iso_speed_rating"] = exif_info['ISOSpeedRatings'] #iso
                #photo_info["metering_mode"] = exif_info['MeteringMode']  #测光模式
                #photo_info["exposure_program"] = exif_info['ExposureProgram'] #曝光程序
                photo_info["focal_length"] = (lambda x:float('%0.1f'%(float(x[0])/float(x[1]))))(exif_info['FocalLength']) #焦距
            except KeyError,e:
                log.warning(e)
                photo_info['has_exif'] = "false"
                
        else:
            photo_info['has_exif'] = "false"

        self.render('photo_info.html',photo_info=photo_info,comments = self.get_comment_by_pid(pid))

    def get_comment_by_pid(self,pid):
        
        comments = self.db.comment.find({"p_id":pid})

        cs_dict = {}
        cs_list = []

        index = 1
        for c in comments:
            u = self.db.user.find_one({"user_id":c['uid']})
            cs_dict = {
                "index":index,
                "uid":c['uid'],
                "avatar":u['avatar'],
                "name":u['name'],
                "content":c['content'],
                "submit_time":c['submit_time']
            }
            cs_list.append(cs_dict)
            index = index + 1
        return cs_list

    def get_exif_info(self,photo):
        sio = StringIO.StringIO(photo.read())
        sio_photo = Image.open(sio)
        try:
            exif_info = sio_photo._getexif()
        except AttributeError,e:
            return None

        if not exif_info:
            return None
        ret = {} 
        for tag,value in exif_info.items():
            decoded = TAGS.get(tag,tag)
            ret[decoded] = value
        sio.close()
        #print ret
        log.info(ret)
        return ret



