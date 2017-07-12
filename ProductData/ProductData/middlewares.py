# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from .settings import PROXIES
import random

class RandomProxy(object):
    """
    设置代理IP
    """
    def process_request(self,request,spider):
        proxy = random.choice(PROXIES)
        request.meta['proxy'] = "http://" + proxy['ip_port']

