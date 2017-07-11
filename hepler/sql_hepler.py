# !/usr/bin/env python
# -*- coding:utf-8 -*-
from hepler import config,log_helper
import redis
import json
import logging


def save_to_redis(p_url,data,save_to_mysql=True):
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
            # 将数据保存到mysql
            pass

        p_redis.rpush(p_url,json.dumps(data))

    except Exception as e:
        log_helper.log(e,level=logging.WARNING)