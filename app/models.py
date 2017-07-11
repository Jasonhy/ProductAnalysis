from django.db import models

# Create your models here.
class ProductInfo(models.Model):
    """
    产品信息
    """
    p_url = models.CharField(max_length=256,name='p_url',verbose_name='产品url')
    p_title = models.CharField(max_length=32,name='p_title',verbose_name='产品名称')
    p_img = models.CharField(max_length=256,name='p_img',verbose_name='产品图片')

    p_price_in_jd = models.CharField(max_length=32,name='p_price_in_jd',verbose_name='京东')
    p_price_in_tmall = models.CharField(max_length=32,name='p_price_in_tmall',verbose_name='天猫')
    p_price_in_zol = models.CharField(max_length=32,name='p_price_in_zol',verbose_name='zol')

    p_c_score = models.FloatField(name='p_c_score', verbose_name='产品总评分', null=True,blank=True)
    p_c_good_nums = models.IntegerField(name='p_c_good_nums', verbose_name='产品好评数', null=True,blank=True)
    p_c_mid_nums = models.IntegerField(name='p_c_mid_nums', verbose_name='产品中评数', null=True,blank=True)
    p_c_bad_nums = models.IntegerField(name='p_c_bad_nums', verbose_name='产品差评数', null=True,blank=True)

    p_c_all_nums = models.CharField(max_length=256,name='p_c_all_nums',verbose_name='概况点评内容',null=True,blank=True)

    class Meta:
        db_table = 'product_info'
        verbose_name_plural = '产品信息'

    def __str__(self):

        return self.p_title


class ProductCommentTime(models.Model):
    """
    产品评论日期
    """
    p_c_time = models.CharField(max_length=32,name='p_c_time',verbose_name='产品评论日期', null=True,blank=True)
    p_info_id = models.ForeignKey('ProductInfo',name='p_info_id',verbose_name='所属产品', null=True,blank=True)

    class Meta:
        db_table = 'product_comment_time'
        verbose_name_plural = '评论日期'

    def __str__(self):

        return self.p_c_time