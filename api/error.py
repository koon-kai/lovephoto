# -*- coding: utf-8 -*-
import datetime
#from model.user import User

class OAuthError(Exception):
    def __init__(self, msg_type, user_id, openid_type, msg):
        self.msg_type = msg_type
        self.user_id = user_id
        self.openid_type = openid_type
        self.msg = msg

    def __str__(self):
        return "OAuthError: user:%s, openid_type:%s, %s, %s" % \
            (self.user_id, self.openid_type, self.msg_type, self.msg)
    __repr__ = __str__


class OAuthTokenExpiredError(OAuthError):
    TYPE = "expired"
    def __init__(self, user_id=None, openid_type=None, msg=""):
        super(OAuthTokenExpiredError, self).__init__(
            OAuthTokenExpiredError.TYPE, user_id, openid_type, msg)

class OAuthAccessError(OAuthError):
    TYPE = "access_error"
    def __init__(self, user_id=None, openid_type=None, msg=""):
        super(OAuthAccessError, self).__init__(
            OAuthTokenExpiredError.TYPE, user_id, openid_type, msg)


class OAuthLoginError(OAuthError):
    TYPE = "login"
    def __init__(self, user_id=None, openid_type=None, msg=""):
        super(OAuthLoginError, self).__init__(
            OAuthLoginError.TYPE, user_id, openid_type, msg)

