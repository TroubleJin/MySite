#!/usr/bin/env python
# coding=utf-8

from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination
from utils.apiresponse import ApiResponse
class Pagenation(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 5

class OffsetPagination(LimitOffsetPagination):
    default_limit =  3
    max_limit = 3
    limit_query_param = 'limit'
    offset_query_param =  'offset'

class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return ApiResponse({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })