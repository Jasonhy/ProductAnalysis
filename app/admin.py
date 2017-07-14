from django.contrib import admin
from . import models
# Register your models here.

class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ('p_title','p_c_score','p_id')

admin.site.register(models.ProductInfo,ProductInfoAdmin)

