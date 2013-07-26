#!/usr/bin/env python
# coding=utf-8

import tornado.web
from tornado.escape import json_decode
from utils.tools import format_datetime2str,format_str2datetime
from utils.logger import logging

log = logging.getLogger(__name__)

class BaseHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    @property
    def fs(self):
        return self.application.fs

    #@property
    #def cache(self):
    #    return self.application.cache

    @property
    def mc(self):
        return self.application.mc

    @property
    def thumb_dir(self):
        return self.application.settings['thumb_dir']

    @property
    def site_path(self):
        return self.application.settings['site_path']

    def get_current_user(self):
        user = self.get_secure_cookie("user")
        if not user: 
            return None
        return user

    def currentUserGet(self):
        '''
        get user info from cookie.
        '''
        pass

    def currentUserSet(self,user):
        '''
        set user info to cookie.
        '''
        if user:
            self.set_secure_cookie("user",tornado.escape.json_encode(user),1)
        else:
            self.clear_cookie("user")

    def render(self, template_name, **template_vars):
        template_vars['json_decode'] = json_decode
        template_vars['format_datetime2str'] = format_datetime2str
        template_vars['format_str2datetime'] = format_str2datetime
        super(BaseHandler, self).render(template_name, **template_vars)
        
    def get_request_files(self,form_name):
        '''
        限制上传的文件类型（只能是图片格式）
        '''
        files = list()
        allowed_mimetypes = (
                'image/jpeg', 
                'image/png', 
                'image/gif',
                'image/x-ms-bmp', 
                'image/efax',
                )
        try:
            for f in self.request.files[form_name]:
                if f.get('content_type') not in allowed_mimetypes:
                    raise AssertionError("Mimetype %s is not supported or allowed." % f.get('content_type'))
                files.append(f)
        except KeyError,e:
            log.error(e)
            # No files uploaded
            return files

        return files


    def gen_error(self, status_code=500, **kwargs):

        import sys
        exc_type, exc_value, exc_tb = sys.exc_info()
        self.send_error(status_code = status_code, exc_info = (exc_type, exc_value, exc_tb))

    def write_error(self, status_code, **kwargs):

        error = status_code
        trace_info = ""
        error_info = "Error occured while %s %s" % (self.request.method, self.request.full_url())

        import traceback
        if self.settings.get("debug") and "exc_info" in kwargs:
            exc_info = kwargs['exc_info']
            #trace_info = ''.join(["%s<br/>" % line for line in traceback.format_exception(*exc_info)])
            trace_info = traceback.format_exception(*exc_info)[-1]
            if not error:
                error = exc_info[1]

        self.set_header("Content-Type", "text/html")
        self.render("error.html", error=error,error_info = error_info, trace_info = trace_info)
