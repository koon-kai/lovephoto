#-*- coding:utf-8 -*-

import re
import time
import datetime
import hashlib

import config
from tornado.escape import json_decode

## User数据接口 
class AbsUserData(object):

    def __init__(self, data):
        if data:
            self.data = data
        else:
            self.data = {}
        if isinstance(data, basestring):
            self.data = json_decode(data)

    def get_user_id(self):
        raise NotImplementedError

    def get_uid(self):
        raise NotImplementedError

    def get_nickname(self):
        return ""

    def get_intro(self):
        return ""

    def get_signature(self):
        return ""

    def get_avatar(self):
        return ""

    def get_icon(self):
        return ""
    
    def get_email(self):
        return ""

## 豆瓣user数据接口
class DoubanUser(AbsUserData):
    def __init__(self, data):
        super(DoubanUser, self).__init__(data)

    def get_user_id(self):
        id_ = self.data.get("id", {}).get("$t")
        if id_:
            return (id_.rstrip("/").split("/"))[-1]
        return None

    def get_uid(self):
        return self.data.get("uid", {}).get("$t")

    def get_nickname(self):
        return self.data.get("title", {}).get("$t")

    def get_intro(self):
        return self.data.get("content", {}).get("$t")

    def get_signature(self):
        return self.data.get("signature", {}).get("$t")

    def get_avatar(self):
        icon = self.get_icon()
        user_id = self.get_user_id()

        return icon.replace(user_id, "l%s" % user_id)

    def get_icon(self):
        links = {}
        _links = self.data.get("link", [])
        for x in _links:
            rel = x.get("@rel")
            links[rel] = x.get("@href")
        return links.get("icon", "")

## 豆瓣user2数据接口
class DoubanUser2(AbsUserData):
    def __init__(self, data):
        super(DoubanUser2, self).__init__(data)

    def get_user_id(self):
        return self.data.get("id")

    def get_uid(self):
        return self.data.get("uid")

    def get_nickname(self):
        return self.data.get("screen_name")

    def get_intro(self):
        return self.data.get("description")

    def get_signature(self):
        return ""

    def get_avatar(self):
        return self.data.get("large_avatar")

    def get_icon(self):
        return self.data.get("small_avatar")

## 新浪微博user数据接口
class SinaWeiboUser(AbsUserData):

    def __init__(self, data):
        super(SinaWeiboUser, self).__init__(data)

    def get_user_id(self):
        return self.data.get("idstr","")

    def get_uid(self):
        return self.data.get("domain", "")

    def get_nickname(self):
        return self.data.get("screen_name", "")

    def get_intro(self):
        return self.data.get("description", "")

    def get_signature(self):
        return ""

    def get_avatar(self):
        return self.data.get("avatar_large", "")

    def get_icon(self):
        return self.data.get("profile_image_url", "")

    def get_email(self):
        return ""


## 第三方数据接口
class AbsData(object):
    
    def __init__(self, site, category, data):
        self.site = site
        self.category = category
        self.data = data or {}
        if isinstance(data, basestring):
            try:
                self.data = json_decode(data)
            except Exception, e:
                #import traceback; print traceback.format_exc()
                self.data = {}

    ## 注释以微博为例
    ##原始的数据，json_decode之后的
    def get_data(self):
        return self.data
    
    ##原微博的id
    def get_origin_id(self):
        raise NotImplementedError
    
    ##原微博的创建时间
    def get_create_time(self):
        raise NotImplementedError
    
    ##如果有title的话，比如豆瓣广播
    def get_title(self):
        return ""

    ##原微博的内容
    def get_content(self):
        return ""

    ##原微博本身是个转发，获取被转发的内容
    def get_retweeted_data(self):
        return None

    ##原微博附带的图片，返回结果为list
    def get_images(self):
        return []
    
    ##原微博的作者，如果能获取到的话
    ##XXX
    def get_user(self):
        return None

    ##原微博的uri，可以点过去查看（有可能获取不到或者很麻烦，比如sina就很变态）
    ###XXX
    def get_origin_uri(self):
        return ""

    ##摘要信息，对于blog等长文来说很有用,视情况在子类中覆盖该方法
    def get_summary(self):
        return self.get_content()

    ##lbs信息
    def get_location(self):
        return ""

    ##附件信息(暂时只有豆瓣的有)
    def get_attachments(self):
        return None

class DoubanData(AbsData):
    
    def __init__(self, category, data):
        super(DoubanData, self).__init__( 
                config.OPENID_TYPE_DICT[config.OPENID_DOUBAN], category, data)


class _Attachment(object):
    def __init__(self, data):
        self.data = data or {}

    def get_description(self):
        return self.data.get("description")
    def get_title(self):
        return self.data.get("title", "")
    def get_href(self):
        return self.data.get("expaned_href") or self.data.get("href")
    def get_medias(self):
        rs = self.data.get("media", [])
        return [_Media(x) for x in rs]


class _Media(object):
    def __init__(self, data):
        self.data = data or {}

    def get_type(self):
        return self.data.get("type")
    def get_src(self):
        src = self.data.get("original_src", "") or self.data.get("src", "")
        return src.replace("/spic/", "/mpic/").replace("/small/", "/raw/")
    
class SinaWeiboData(AbsData):
    
    def __init__(self, category, data):
        super(SinaWeiboData, self).__init__( 
                config.OPENID_TYPE_DICT[config.OPENID_SINA], category, data)

# 新浪微博status
class SinaWeiboStatusData(SinaWeiboData):
    def __init__(self, data):
        super(SinaWeiboStatusData, self).__init__(
                config.CATE_SINA_STATUS, data)
    
    def get_origin_id(self):
        return self.data.get("idstr", "")

    def get_create_time(self):
        try:
            t = self.data.get("created_at", "")
            return datetime.datetime.strptime(t, "%a %b %d %H:%M:%S +0800 %Y")
        except Exception, e:
            print e
            return None
    
    def get_title(self):
        return ""

    def get_content(self):
        return self.data.get("text", "") 
    
    def get_retweeted_data(self):
        re = self.data.get("retweeted_status")
        if re:
            return SinaWeiboStatusData(re)

    def get_user(self):
        return SinaWeiboUser(self.data.get("user"))

    def get_origin_pic(self):
        return re.sub("ww[23456].sinaimg.cn", "ww1.sinaimg.cn", self.data.get("original_pic", ""))

    def get_thumbnail_pic(self):
        return re.sub("ww[23456].sinaimg.cn", "ww1.sinaimg.cn", self.data.get("thumbnail_pic", ""))

    def get_middle_pic(self):
        return re.sub("ww[23456].sinaimg.cn", "ww1.sinaimg.cn", self.data.get("bmiddle_pic", ""))

    def get_images(self, size="origin"):
        method = "get_%s_pic" % size
        if hasattr(self, method):
            i = getattr(self, method)()
            if i:
                return [i]
        return []
        
