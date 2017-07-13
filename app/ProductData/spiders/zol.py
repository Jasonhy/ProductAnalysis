# -*- coding: utf-8 -*-
import logging
import re

import scrapy
from scrapy import Request

from .. import config,log_helper
from ..items import ProductdataItem

class ZolSpider(scrapy.Spider):
    name = 'zol'
    allowed_domains = ['detail.zol.com.cn']
    base_url = "http://detail.zol.com.cn"
    url = base_url + "/subcategory.html"

    def start_requests(self):
        yield Request(
            url=self.url,
            headers=config.headers,
            method='GET',
            callback=self.get_type_product,
        )

    def get_type_product(self,response):
        """
        获取分类类别
        :param response:
        :return:
        """
        type_urls = response.xpath("//div[@class='subcate-list']/a/@href").extract()
        page_urls = response.xpath("//div[@class='pagebar']/a/@href").extract()

        for type_url in type_urls:
            # 对每一个url发送请求

            yield Request(
                url=self.base_url + type_url,
                headers=config.headers,
                method='GET',
                callback=self.get_product_list,
            )

        # 对分页进行递归
        # all_page_num = int("".join(response.xpath("//div[@class='small-page']/span/text()").extract()).replace("/","").strip())
        # cur_page = int("".join(response.xpath("//div[@class='small-page']/span/b/text()").extract()).strip())

        for p in page_urls:
            # 判断当前页和总页数的差值
            # if cur_page <= all_page_num:
            #     yield Request(
            #         url=self.base_url + p,
            #         headers=config.headers,
            #         method='GET',
            #         callback=self.get_type_product,
            #     )
            yield Request(
                url=self.base_url + p,
                headers=config.headers,
                method='GET',
                callback=self.get_type_product,
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

        try:
            p_nums = len(p_urls)
            for i in range(p_nums):
                p_url = p_urls[i]
                res = re.findall(r'(\d+)', p_url)
                if len(res) > 0:
                    p_id = res[-2]
                else:
                    p_id = res[-1]

                product_info = {
                    'p_url':self.base_url + p_url,
                    'p_title':p_titles[i],
                    'p_c_score':p_scores[i],
                    'p_id':p_id
                }

                yield Request(
                    url=self.base_url + p_urls[i],
                    headers=config.headers,
                    method='GET',
                    meta=product_info,
                    callback=self.get_product_info,
                )

        except Exception as e:

            log_helper.log(e, logging.WARNING)

    def get_product_info(self,response):
        """
        获取每个产品信息
        :param response:
        :return:
        """
        comment_url = "".join(response.xpath("//ul[@class='nav']/li/a[@class='ol-comment']/@href").extract())
        p_img = "".join(response.xpath("//div[@class='bigpic']/a/img/@src").extract())
        p_prices = response.xpath("//div[@class='product-merchant-price clearfix']/ul/li/strong/a/text() | //div[@class='product-merchant-price clearfix']/ul/li/span/a/text()").extract()

        response.meta['p_img'] = p_img
        response.meta['p_prices'] = p_prices

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
        """
        product_info = response.meta

        item = ProductdataItem()
        item['p_url'] = product_info['p_url']
        item['p_title'] = product_info['p_title']
        item['p_c_score'] = product_info['p_c_score']
        item['p_prices'] = "".join(product_info['p_prices']) if product_info['p_prices'] else "价格未知"
        item['p_img'] = product_info['p_img']
        item['p_id'] = product_info['p_id']
        item['p_c_all_nums'] = "".join(p_c_all_nums)
        item['p_comments'] = "".join(p_comments).replace(" ","").replace("\r\n","")
        item['p_c_times'] = p_c_times

        yield item









