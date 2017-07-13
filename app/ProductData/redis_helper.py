# !/usr/bin/env python
# -*- coding:utf-8 -*-
import redis
from . import config
from .sql_hepler import SqlHelper
import json

p_redis = redis.StrictRedis(host=config.redis_host, port=config.redis_port)
p_sql = SqlHelper()

def save_to_redis(item,save_to_mysql=False):
    """
    保存数据的redis
    :param data: 需要保存的数据
    :param save_to_mysql: 是否将数据保存的mysql数据库
    :return:
    """
    """
       p_url
       p_title
       p_c_score
       p_img
       p_prices
       p_c_all_nums
       p_comments
       p_c_times
       p_id
    """
    if save_to_mysql:
        product_info = {
            'p_url':item['p_url'],
            'p_title':item['p_title'],
            'p_img':item['p_img'],
            'p_id':item['p_id'],
            'p_prices':item['p_prices'],
            'p_c_score':item['p_c_score'],
            'p_comments':item['p_comments'],
            'p_c_all_nums':item['p_c_all_nums'],
        }
        p_sql.insert_json(product_info,config.product_info)

    p_redis.rpush(item['p_id'],json.dumps(item))