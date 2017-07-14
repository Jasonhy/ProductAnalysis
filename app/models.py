from django.db import models

# Create your models here.
class ProductInfo(models.Model):
    """
    产品信息
    """
    p_url = models.CharField(max_length=256,name='p_url',verbose_name='产品url')
    p_title = models.CharField(max_length=64,name='p_title',verbose_name='产品名称')
    p_img = models.CharField(max_length=256,name='p_img',verbose_name='产品图片')
    p_id = models.IntegerField(name='p_id',verbose_name='产品ID')

    p_prices= models.CharField(max_length=128,name='p_prices',verbose_name='商品价格', null=True,blank=True)

    p_c_score = models.FloatField(name='p_c_score', verbose_name='产品总评分', null=True,blank=True)
    p_comments = models.CharField(max_length=128,name='p_comments', verbose_name='产品评价', null=True,blank=True)

    p_c_all_nums = models.CharField(max_length=256,name='p_c_all_nums',verbose_name='概况点评内容',null=True,blank=True)

    p_c_time = models.CharField(max_length=128, name='p_c_time', verbose_name='产品评论日期', null=True, blank=True)

    p_price_trend = models.CharField(max_length=128,name='p_price_trend',verbose_name='价格趋势',null=True,blank=True)

    class Meta:
        db_table = 'product_info'
        verbose_name_plural = '产品信息'

    def __str__(self):

        return self.p_title
