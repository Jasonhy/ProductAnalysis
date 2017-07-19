# !/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
import datetime
import pandas as pd
from hepler import redis_helper,file_hepler
from bokeh.plotting import figure,show,output_file

mpl.rcParams['font.sans-serif'] = ['SimHei']    # 显示中文
mpl.rcParams['font.serif'] = ['SimHei']         # 显示中文
mpl.rcParams['axes.unicode_minus'] = False      # 负号'-'正常显示
import json


def make_comment_plot(data,p_id):
    """
    生成好评率的饼图
    :param datas:
    :return:
    """
    if data:
        temps = "".join(data).replace(" ", "").replace("\r\n", "")
        values = re.findall(r'(\d+)', temps)
        c_values = [int(value) for value in values]
        c_keys = re.findall('[\u4e00-\u9fa5]+', temps)
        print(c_keys)
        s = pd.Series(c_values, index=c_keys,name='好评率')
        s = s[3:6]
        s_sum = s.sum()
        s = s.apply(lambda x: x / s_sum)
        s.plot.pie(autopct='%0.2f%%', fontsize=8, colors=['g', 'y', 'r'])
        plt.savefig("static/upload/%s_c.png" % p_id,dpi=90)
        plt.close()

        return file_hepler.get_image_path("%s_c.png" % p_id)
    else:
        return file_hepler.get_image_path("no_good_comments.png")

def make_overview_plot(data,p_id):
    """
    评价概览
    :param datas:
    :return:
    """
    if data:
        temps = "".join(data)
        values = re.findall(r'(\d+)', temps)
        c_values = [int(value) for value in values]
        c_keys = re.findall('[\u4e00-\u9fa5]+', temps)
        s = pd.Series(c_values, index=c_keys)
        s.plot.bar(figsize=(6, 8), fontsize=8)

        plt.savefig("static/upload/%s_o.png" % p_id,dpi=90)
        plt.close()
        return file_hepler.get_image_path("%s_o.png" % p_id)
    else:
        return file_hepler.get_image_path("no_overview.png")

def make_hot_plot(data,p_id):
    """
    根据评价最近评价来判断这个产品是否是热门
    :param datas:
    :return:
    """
    if data:
        data = data.split(",")
        dt1 = datetime.datetime.now()
        temp = list(set(data))
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
        df.plot(subplots=True)
        plt.savefig("static/upload/%s_h.png" % p_id,dpi=90)
        return file_hepler.get_image_path("%s_h.png" % p_id)
    else:
        return file_hepler.get_image_path("no_hot.png")


