from django.shortcuts import render
import pandas as pd
import json
import codecs
import re


# Create your views here.

def index(request):
    with codecs.open('/static/file/product_info.json', 'r',encoding='utf-8') as file:
        datas = json.load(file)

    temps = datas[0]['p_c_all_nums']
    values = []
    keys = []
    for i in range(len(temps)):
        if i % 2 == 0:
            keys.append(temps[i])
        else:
            values.append(int(re.search(r"(\d+)", temps[i]).group(0)))
    df = pd.DataFrame(values, index=keys)


    return render(request,'index.html')
