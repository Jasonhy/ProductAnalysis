# !/usr/bin/env python
# -*- coding:utf-8 -*-
productanalysis_db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'charset': 'utf8',
}

productanalysis_db = 'productanalysis'

product_info = 'product_info'
product_comment_time = 'product_comment_time'
product_analysis_image = 'product_analysis_image'

# 请求的header
headers = {
        "Host": "detail.zol.com.cn",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Upgrade-Insecure-Requests": 1,
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        "Accept": "text/html, application/xhtml + xml, application/xml;q = 0.9, image/webp, * / *;q = 0.8",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8",
    }

# redis
redis_pass = ''
redis_host = 'localhost'
redis_part = '6397'
redis_db = 10