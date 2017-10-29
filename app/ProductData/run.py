# !/usr/bin/env python
# -*- coding:utf-8 -*-
from scrapy import cmdline


def cmd():
    cmdline.execute("scrapy crawl zol".split())

if __name__ == '__main__':
    cmd()