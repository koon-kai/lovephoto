#!/usr/bin/env python
# coding=utf-8

import base


class PageNotFoundHandler(base.BaseHandler):
    def get(self):
        self.gen_error(status_code=404)

