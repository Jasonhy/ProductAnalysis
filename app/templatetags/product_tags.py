# !/usr/bin/env python
# -*- coding:utf-8 -*-
from django.utils.safestring import mark_safe
from django import template
register = template.Library()

@register.simple_tag
def get_search_result_list(product_list):
    """
    获取搜索产品列表
    :param product_list:
    :return:
    """
    res = ""
    if product_list:
        for index in range(len(product_list)):
            if index == 0:
                res = ' <li class="active"><a id="set_click" href="javascript:;" onclick="get_plot(%s,this)">%s</a></li>' % (product_list[index].object.p_id,product_list[index].object.p_title)
            else:
                res += ' <li><a href="javascript:;" onclick="get_plot(%s,this)">%s</a></li>' % (product_list[index].object.p_id,product_list[index].object.p_title)
    else:
        res = '<li><a href="javascript:void(0);">未找到相应的结果</a></>'

    return mark_safe(res)

