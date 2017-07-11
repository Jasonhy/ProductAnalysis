# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductdataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    """
    p_url
    p_title
    p_c_score
    p_img
    p_prices
    p_c_all_nums
    p_comments
    p_c_times
    """

    p_url = scrapy.Field()
    p_title = scrapy.Field()
    p_c_score = scrapy.Field()
    p_img = scrapy.Field()
    p_prices = scrapy.Field()
    p_c_all_nums = scrapy.Field()
    p_comments = scrapy.Field()
    p_c_times = scrapy.Field()

