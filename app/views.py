from django.shortcuts import render
from django.http import JsonResponse
import json
from hepler import make_plot_helper
from app.models import ProductInfo
from multiprocessing import Pool

def index(request):

    return render(request, 'index.html')


def make_plot(request):
    """
    生成分析图片
    :param request:
    :return:
    """
    # 通过线程池来存储图片
    pool = Pool(10)

    p_id = int(request.POST.get('p_id'))
    result = {
        'status':1,
    }

    product_info = ProductInfo.objects.get(p_id=p_id)

    pool.apply(make_plot_helper.make_comment_plot,args=(product_info.p_comments,p_id))
    pool.apply(make_plot_helper.make_overview_plot,args=(product_info.p_c_all_nums,p_id))
    pool.apply(make_plot_helper.make_hot_plot,args=(product_info.p_c_time,p_id))
    pool.close()
    pool.join()

    return JsonResponse(result)

