from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.

def index(request):

    return render(request, 'index.html')


def make_plot(request):
    """
    生成分析图片
    :param request:
    :return:
    """

    return JsonResponse("{'msg':'ok'}")

