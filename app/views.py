from django.shortcuts import render
import pandas as pd
import json
import codecs
import re
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
import datetime

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['font.serif'] = ['SimHei']

# Create your views here.

def index(request):
    with codecs.open('static/file/product_info.json', 'r',encoding='utf-8') as file:
        datas = json.load(file)


    return render(request,'index.html')



