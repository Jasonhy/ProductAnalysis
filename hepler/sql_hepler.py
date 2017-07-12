# !/usr/bin/env python
# -*- coding:utf-8 -*-
from hepler import config,log_helper
import json
import logging
import redis
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ProductAnalysis.settings")
django.setup()
from app.models import ProductInfo,ProductCommentTime

def save_to_redis(item,save_to_mysql=True):
    """
    保存数据的redis
    :param data: 需要保存的数据
    :param save_to_mysql: 是否将数据保存的mysql数据库
    :return:
    """
    try:
        p_redis = redis.StrictRedis(host=config.redis_host, port=config.redis_part,
                                    db=config.redis_db, password=config.redis_pass)

        if save_to_mysql:
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
            # 将数据保存到mysql
            product_info = ProductInfo()
            product_info.p_url = item['p_url']
            product_info.p_title = item['p_title']
            product_info.p_c_score = item['p_c_score']
            product_info.p_img = item['p_img']
            product_info.p_prices = item['p_prices']
            product_info.p_c_all_nums = item['p_c_all_nums']
            product_info.p_comments = item['p_comments']
            product_info.p_id = item['p_id']
            product_info.save()

            for t in item['p_c_times']:
                product_comment = ProductCommentTime()
                product_comment.p_c_time = t
                product_comment.p_info = product_info
                product_comment.save()

        data = json.dumps(item)
        p_redis.rpush(item['p_id'],data)

    except Exception as e:
        log_helper.log(e,level=logging.WARNING)