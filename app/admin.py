from django.contrib import admin
from . import models
# Register your models here.

class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ('p_title','p_c_score','p_c_good_nums','p_c_mid_nums','p_c_bad_nums')

class ProductCommentTimeAdmin(admin.ModelAdmin):
    list_display = ('p_info_id','p_c_time')

admin.site.register(models.ProductInfo,ProductInfoAdmin)
admin.site.register(models.ProductCommentTime,ProductCommentTimeAdmin)
