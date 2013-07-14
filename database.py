#!/usr/bin/env python
# coding: utf-8

import logging
#import torndb

#import MySQLdb

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

import redis
from redis.connection import ConnectionError

from config import *
import config



""" Connect to MySql db """
#db_conn = None
#try:
#    db_conn =  torndb.Connection(
#         host = config.DB_HOST, database =  config.DB_NAME,
#         user = config.DB_USER, password = config.DB_PASSWD
#    )
#except Exception,e:
#    logging.error("Cannot connect to MySQL on %s", config.DB_HOST, exc_info=True)
#    raise e

#def connect_db():
#    try:
#        conn = MySQLdb.connect(
#            host=config.DB_HOST,
#            port=config.DB_PORT,
#            user=config.DB_USER,
#            passwd=config.DB_PASSWD,
#            db=config.DB_NAME,
#            use_unicode=True,
#            charset="utf8")
#        return conn
#    except Exception, e:
#        print "connect db fail:%s" % e
#        return None
#
#
#class DB(object):
#    
#    def __init__(self):
#        self._conn = connect_db()
#
#    def connect(self):
#        self._conn = connect_db()
#        return self._conn
#
#    def execute(self, *a, **kw):
#        cursor = kw.pop('cursor', None)
#        try:
#            cursor = cursor or self._conn.cursor()
#            cursor.execute(*a, **kw)
#        except (AttributeError, MySQLdb.OperationalError):
#            print 'debug, %s re-connect to mysql' % datetime.datetime.now()
#            self._conn and self._conn.close()
#            self.connect()
#            cursor = self._conn.cursor()
#            cursor.execute(*a, **kw)
#        return cursor
#        
#    def commit(self):
#        return self._conn and self._conn.commit()
#
#    def rollback(self):
#        return self._conn and self._conn.rollback()
#
#db_conn = DB()



""" Connct to MongoDB """
mongo_client = None
try:
    mongo_client = MongoClient(host=MONGO_HOST,port=MONGO_PORT)
    print "MongoDB Connected successfully"
except ConnectionError, e:
    sys.stderr.write("Could not connect to MongoDB:%s\n" % e)
    #sys.exit(1)


""" Connct to Redis """
redis_conn = None
try:
    pool = redis.ConnectionPool(host=REDIS_HOST,port=REDIS_PORT,db=REDIS_DB)
    redis_conn = redis.Redis(connection_pool=pool)
    redis_conn.ping()
    print "Redis Connected successfully"
except ConnectionError,e:
    sys.stderr.write("Could not connect to Redis:%s\n" % e)

