# -*- coding: utf-8 -*-
# @Time    : 2020-03-24 11:55
# @Author  : ken
'''

'''
import redis
from config import redis_db, redis_host, redis_pass, redis_port


class RedisObject:
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = object.__new__(cls)
        return cls._instance

    def get_connection(self):
        '''获取redis连接'''
        # redis_host, redis_pass, redis_port, redis_db = '', '', '', ''
        pool = redis.ConnectionPool(host=redis_host, password=redis_pass, port=redis_port, db=redis_db, socket_timeout=5, max_connections=469)
        conn = redis.StrictRedis(connection_pool=pool, decode_responses=True)
        return conn
