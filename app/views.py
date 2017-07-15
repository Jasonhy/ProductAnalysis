from django.shortcuts import render
from django.http import JsonResponse
import json
from hepler import make_plot_helper
from app.models import ProductInfo
from multiprocessing import Pool
from hepler import redis_helper,log_helper
import logging

def index(request):

    return render(request, 'index.html')


def make_plot(request):
    """
    生成分析图片
    :param request:
    :return:
    """
    # 通过线程池来存储图片
    pool = Pool(3)

    p_id = int(request.POST.get('p_id'))

    images = []
    result = {
        'status':1,
    }
    """
    {
        p_id:{
            "p_url":
            "p_title":
            "p_img":
            "p_price":
            "p_c_score":
            "p_analysis_imgs":[]
        }
    }

    """
    # 先从redis里获取数据,如果数据不存在再从mysql数据获取
    try:
        res = redis_helper.p_redis.get(p_id)
    except Exception as e:
        res = None
    if res:
        p_info = json.dumps(res.decode(encoding='utf-8'),ensure_ascii=False)
    else:
        try:
            product_info = ProductInfo.objects.get(p_id=p_id)
            p_url = product_info.p_url
            p_title = product_info.p_title
            p_img = product_info.p_img
            p_prices = product_info.p_prices
            p_c_score = product_info.p_c_score
            if not p_c_score:
                p_c_score = "暂无评分"
            p_info = {
                    "p_id":p_id,
                    "p_url": p_url,
                    "p_title": p_title,
                    "p_img": p_img,
                    "p_price": p_prices,
                    "p_c_score": p_c_score
            }
            images.append(pool.apply_async(make_plot_helper.make_comment_plot,args=(product_info.p_comments,p_id)))
            images.append(pool.apply_async(make_plot_helper.make_overview_plot,args=(product_info.p_c_all_nums,p_id)))
            images.append(pool.apply_async(make_plot_helper.make_hot_plot,args=(product_info.p_c_time,p_id)))
            pool.close()
            pool.join()

            p_info["p_analysis_imgs"] = [img.get() for img in images]

            # 将数据保存到redis
            redis_helper.save_to_redis(p_info)

        except Exception as e:
            result["error_msg"] = "暂无此产品"
            result["status"] = 0
            p_info = {}
            log_helper.log(e,logging.WARNING)


    result['data'] = p_info

    return JsonResponse(result)

