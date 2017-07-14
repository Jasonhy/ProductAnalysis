# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from . import redis_helper,config
from .sql_hepler import SqlHelper
p_sql = SqlHelper()

class ProductdataPipeline(object):

    def process_item(self, item, spider):
        """
        将数据保存到mysql数据库
        :param item:
        :param spider:
        :return:
        """
        item = dict(item)
        product_info = {
            'p_url': item['p_url'],
            'p_title': item['p_title'],
            'p_img': item['p_img'],
            'p_id': item['p_id'],
            'p_prices': item['p_prices'],
            'p_c_score': item['p_c_score'],
            'p_comments': item['p_comments'],
            'p_c_all_nums': item['p_c_all_nums'],
            'p_c_time': item['p_c_times'],
            'p_price_trend': item['p_price_trend'],
        }
        p_sql.insert_json(product_info, config.product_info)

        return item