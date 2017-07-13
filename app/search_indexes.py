# !/usr/bin/env python
# -*- coding:utf-8 -*-
from haystack import indexes
from app.models import ProductInfo

class ProductInfoSearch(indexes.SearchIndex,indexes.Indexable):
    """
    全文搜索
    """
    text = indexes.CharField(document=True,use_template=True)

    def get_model(self):

        return ProductInfo

    def index_queryset(self, using=None):

        return self.get_model().objects.all()