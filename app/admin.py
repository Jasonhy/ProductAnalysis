from django.contrib import admin
from . import models
# Register your models here.

class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ('p_title','p_c_score','p_id')

class ProductCommentTimeAdmin(admin.ModelAdmin):
    list_display = ('p_info_id','p_c_time')

admin.site.register(models.ProductInfo,ProductInfoAdmin)
admin.site.register(models.ProductCommentTime,ProductCommentTimeAdmin)
