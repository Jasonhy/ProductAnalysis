# !/usr/bin/env python
# -*- coding:utf-8 -*-
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.charts import Bar,Line
from hepler import file_hepler
import re
import pandas as pd
import datetime

TOOLS = "save"

def make_commment_bokeh(data):
    if data:
        temps = "".join(data).replace(" ", "").replace("\r\n", "")
        values = re.findall(r'(\d+)', temps)
        c_values = [int(value) for value in values]
        c_keys = re.findall('[\u4e00-\u9fa5]+', temps)    #
        s = pd.Series(c_values, index=c_keys, name='好评率')
        s = s[3:6]
        s_sum = s.sum()
        s = s.apply(lambda x: x / s_sum * 100)
        factors = list(s.index)
        x = s.values
        dot = figure(title="好评率(单位:%)", tools=TOOLS, toolbar_location=None,
                     y_range=factors, x_range=[0, 100],width=400, height=400)
        dot.segment(0, factors, x, factors, line_width=2, line_color="green", )
        dot.circle(x, factors, size=15, fill_color="orange", line_color="green", line_width=3, )
        script, div = components(dot, CDN)

        return [script,div]
    else:
        return [0,file_hepler.get_image_path("no_good_comments.png")]

def make_overview_bokeh(data):
    if data:
        temps = "".join(data)
        values = re.findall(r'(\d+)', temps)
        c_values = [int(value) for value in values]
        c_keys = re.findall('[\u4e00-\u9fa5]+', temps)
        s = pd.Series(c_values, index=c_keys)
        data = s
        # 创建一个新的含有标题和轴标签的窗口在线窗口
        p = Bar(data,title="总览图", ylabel='关键字数量', width=400, height=400,legend=None,tools=TOOLS)
        script, div = components(p, CDN)

        return [script, div]
    else:
        return [0,file_hepler.get_image_path("no_overview.png")]

def make_hot_bokeh(data):
    from bokeh.models import BoxAnnotation
    if data:
        data = data.split(",")
        dt1 = datetime.datetime.now()
        temp = list(set(data))
        sub_dates = [(dt1 - datetime.datetime.strptime(dt, '%Y-%m-%d')).days for dt in temp]

        s = pd.Series(sub_dates, [datetime.datetime.strptime(dt, '%Y-%m-%d') for dt in temp])
        s = s.sort_index(ascending=False)

        p = figure(x_axis_type="datetime", tools=TOOLS,title="热度", x_axis_label='日期', y_axis_label='天数',width=400, height=400)

        p.line(s.index,s.values, legend="距离当前天数", line_width=2)

        script, div = components(p, CDN)

        return [script, div]
    else:
        return [0,file_hepler.get_image_path("no_hot.png")]
