# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from .spiders import sql_hepler

class ProductdataPipeline(object):

    def process_item(self, item, spider):
        """
        将数据保存到redis
        :param item:
        :param spider:
        :return:
        """
        item = dict(item)
        product_info = json.dumps(dict(item),ensure_ascii=False)
        sql_hepler.save_to_redis(item['p_id'],data=product_info)
        return item

