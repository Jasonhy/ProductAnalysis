# !/usr/bin/env python
# -*- coding:utf-8 -*-
import codecs
import re
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
import datetime
import pandas as pd

mpl.rcParams['font.sans-serif'] = ['SimHei']    # 显示中文
mpl.rcParams['font.serif'] = ['SimHei']         # 显示中文
mpl.rcParams['axes.unicode_minus'] = False      # 图像是负号'-'显示为方块的问题

def make_comment_plot(datas):
    """
    生成好评率的饼图
    :param datas:
    :return:
    """
    temps = datas[0]['p_comments']
    temps = "".join(temps).replace(" ", "").replace("\r\n", "")
    values = re.findall(r'(\d+)', temps)
    c_values = [int(value) for value in values]
    c_keys = re.findall('[\u4e00-\u9fa5]+', temps)
    s = pd.Series(c_values, index=c_keys)
    s = s[3:6]
    s_sum = s.sum()
    s = s.apply(lambda x: x / s_sum)
    s.plot.pie(figsize=(8, 8), autopct='%0.2f', fontsize=20, colors=['g', 'y', 'r'])


def make_overview_plot(datas):
    """
    评价概览
    :param datas:
    :return:
    """
    temps = "".join(datas[0]['p_c_all_nums'])
    values = re.findall(r'(\d+)', temps)
    c_values = [int(value) for value in values]
    c_keys = re.findall('[\u4e00-\u9fa5]+', temps)
    s = pd.Series(c_values, index=c_keys)
    s.plot.bar(figsize=(8, 8), fontsize=18)


def make_hot_plot(datas):
    """
    根据评价最近评价来判断这个产品是否是热门
    :param datas:
    :return:
    """
    temp = datas[0]['p_c_times']
    dt1 = datetime.datetime.now()
    temp = list(set(temp))
    sub_dates = [(dt1 - datetime.datetime.strptime(dt, '%Y-%m-%d')).days for dt in temp]
    actives = []
    for d in sub_dates:
        if d <= 360:
            actives.append(100)
        elif 360 < d <= 500:
            actives.append(60)
        else:
            actives.append(0)

    date_dict = {
        'sub_date': sub_dates,
        'active': actives
    }
    df = pd.DataFrame(date_dict, index=temp)
    df.plot(figsize=(8, 8), subplots=True)
