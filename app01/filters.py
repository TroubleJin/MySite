#!/usr/bin/env python
# coding=utf-8


class LimitFilter:
    def filter_queryset(self,request,queryset,view):
        limit = request.query_params.get('limit')
        print(limit)
        if limit:
            limit = int(limit)
            print(limit)
            return queryset[:limit]
        return queryset

from django_filters.rest_framework.filterset import FilterSet
from . import models
from django_filters import filters
# 自定义过滤字段
class SchoolFilterSet(FilterSet):
    min_price = filters.NumberFilter(field_name='f_price',lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='f_price',lookup_expr='lte')
    class Meta:
        models = models.t_school
        fileds = ['min_price','max_price']