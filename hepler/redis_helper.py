# !/usr/bin/env python
# -*- coding:utf-8 -*-
import redis
from . import config
import json

p_redis = redis.StrictRedis(host=config.redis_host, port=config.redis_port)

def save_to_redis(item):
    """
    保存数据的redis
    :param data: 需要保存的数据
    :return:
    """
    p_redis.setex(item['p_id'],config.REDIS_PRODUCT_INFO_EXPIRES_SECONDES,json.dumps(item))