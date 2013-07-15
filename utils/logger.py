#!/usr/bin/env python
#-*- coding:utf-8 -*-

import logging
import config
import os

logging.basicConfig(
        #filename=os.path.join(config.LOG_PATH,'log.txt'),
        format='%(asctime)s %(levelname)s:%(message)s',
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG)

#logging.handlers.TimedRotatingFileHandler
