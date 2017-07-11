# !/usr/bin/env python
# -*- coding:utf-8 -*-
import logging
import datetime

def log(msg,level = logging.DEBUG):
    """
    自定义输出日志
    :param msg: 日志信息
    :param level: 日志等级
    :return:
    """
    logging.log(level,msg)

    print("log时间[%s]-log等级[%s]-log信息[%s]" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),level,msg))
