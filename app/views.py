from django.shortcuts import render
from django.http import JsonResponse
import json
from hepler import make_plot_helper
from app.models import ProductInfo
def index(request):

    return render(request, 'index.html')


def make_plot(request):
    """
    生成分析图片
    :param request:
    :return:
    """
    p_id = int(request.POST.get('p_id'))
    result = {
        'status':1,
    }
    product_info = ProductInfo.objects.get(p_id=p_id)
    make_plot_helper.make_comment_plot(product_info.p_comments,p_id)
    make_plot_helper.make_comment_plot(product_info.p_c_all_nums,p_id)

    return JsonResponse(result)

