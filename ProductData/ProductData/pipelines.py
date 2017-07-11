# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

class ProductdataPipeline(object):
    def __init__(self):
        self.filename = codecs.open('product_info.json','w',encoding='utf8')

    def process_item(self, item, spider):
        product_info = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.filename.write(product_info)

        return item

    def spider_closed(self,spider):

        self.filename.close()
