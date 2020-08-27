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