# -*- coding: utf-8 -*-
import logging
import re

import scrapy
from scrapy import Request
# 使用redis去重
from scrapy.dupefilters import RFPDupeFilter

from .. import config,log_helper
from ..items import ProductdataItem

class ZolSpider(scrapy.Spider):
    name = 'zol'
    allowed_domains = ['detail.zol.com.cn']
    base_url = "http://detail.zol.com.cn"
    urls = ["/notebook_index/subcate16_0_list_1_0_1_2_0_1.html","/cell_phone_index/subcate57_0_list_1_0_1_2_0_1.html","/digital_camera_index/subcate15_0_list_1_0_1_2_0_1.html"]

    def start_requests(self):

        for url in self.urls:
            yield Request(
                url=self.base_url + url,
                headers=config.headers,
                method='GET',
                callback=self.get_product_list,
            )

    def get_product_list(self,response):
        """
        获取每个产品类别下的所有产品
        :param response:
        :return:
        """
        p_urls = response.xpath("//div[@class='pic-mode-box']/ul/li/a/@href").extract()
        p_titles = response.xpath("//div[@class='pic-mode-box']/ul/li/h3/a/text()").extract()
        p_scores = response.xpath("//div[@class='comment-row']/span[@class='score']/text()").extract()

        # 执行分页
        p_pages = response.xpath("//div[@class='pagebar']/a/@href").extract()

        try:
            p_nums = len(p_urls)
            for p_url in p_urls:
                # p_url = p_urls[i]
                res = re.findall(r'(\d+)', p_url)
                if len(res) > 1:
                    p_id = res[-2]
                else:
                    p_id = res[-1]

                product_info = {
                    'p_url':self.base_url + p_url,
                    'p_id':p_id
                }

                yield Request(
                    url=self.base_url + p_url,
                    headers=config.headers,
                    method='GET',
                    meta=product_info,
                    callback=self.get_product_info,
                )

            for p in p_pages:
                # 分页回调
                yield Request(
                    url=self.base_url + p,
                    headers=config.headers,
                    method='GET',
                    callback=self.get_product_list,
                )

        except Exception as e:

            log_helper.log(e, logging.WARNING)

    def get_product_info(self,response):
        """
        获取每个产品信息
        :param response:
        :return:
        """
        p_title = "".join(response.xpath("//div[@class='page-title clearfix']/h1/text()").extract())
        p_c_score = "".join(response.xpath("//div[@class='product-comment']/div/div/div/strong/text()").extract())
        comment_url = "".join(response.xpath("//ul[@class='nav']/li/a[@class='ol-comment']/@href").extract())
        p_img = "".join(response.xpath("//div[@class='bigpic']/a/img/@src").extract())
        p_prices = response.xpath("//div[@class='product-merchant-price clearfix']/ul/li/strong/a/text() | //div[@class='product-merchant-price clearfix']/ul/li/span/a/text()").extract()

        # 参考价
        p_price_retain = ",".join(response.xpath("//div[@class='product-price-info']/div/span/b[@class='price-type price-retain']/text()").extract())
        # 格式 ['[["7.08","7.09","7.10","7.11","7.14"],[2999,2999,2999,2999,2999],2999,2999]']

        p_price_trend = response.xpath("//div[@class='product-price-info']/div/span/b[@class='price-type price-retain']/@chart-data").extract()

        if p_price_trend:
            p_price_trend = p_price_trend[0]

        response.meta['p_img'] = p_img
        response.meta['p_title'] = p_title
        response.meta['p_c_score'] = p_c_score
        response.meta['p_prices'] = p_prices if p_prices else p_price_retain
        response.meta['p_price_trend'] = p_price_trend

        yield Request(
            url=self.base_url + comment_url,
            headers=config.headers,
            method='GET',
            meta=response.meta,
            callback=self.get_product_comment,
        )

    def get_product_comment(self,response):
        """
        获取产品评论信息
        :param response:
        :return:
        """
        p_c_all_nums = response.xpath("//div[@class='good-words']/ul/li/a/text() | //div[@class='good-words']/ul/li/a/span/text()").extract()
        # 所有评论
        p_comments = response.xpath("//div[@class='comment-tabs']/div/label/text() | //div[@class='comment-tabs']/div/label/em/text()").extract()

        # 获取评论日期 这里只获取第一页  获取最新评论日期 来判断这个手机当前的活跃度
        p_c_times = response.xpath("//div[@class='comments-list-content']/div/span[@class='date']/text()").extract()

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
        p_price_trend
        """
        product_info = response.meta

        item = ProductdataItem()
        item['p_url'] = product_info['p_url']
        item['p_title'] = product_info['p_title']
        item['p_c_score'] = product_info['p_c_score']
        item['p_prices'] = "".join(product_info['p_prices']) if product_info['p_prices'] else "暂无报价"
        item['p_img'] = product_info['p_img']
        item['p_id'] = product_info['p_id']
        item['p_c_all_nums'] = "".join(p_c_all_nums)
        item['p_comments'] = "".join(p_comments).replace(" ","").replace("\r\n","")
        item['p_c_times'] = ",".join(p_c_times)
        item['p_price_trend'] = product_info['p_price_trend']

        yield item









