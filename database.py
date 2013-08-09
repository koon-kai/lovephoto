#!/usr/bin/env python
# coding: utf-8


import sys
import config

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


""" Connct to MongoDB """
mongo_client = None
try:
    mongo_client = MongoClient(host=config.MONGO_HOST,port=config.MONGO_PORT)
    print "MongoDB Connected successfully"
except ConnectionFailure, e:
    sys.stderr.write("Could not connect to MongoDB:%s\n" % e)
    #sys.exit(1)


