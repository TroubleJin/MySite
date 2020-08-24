#!/usr/bin/env python
# coding=utf-8

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
class Authentication(BaseAuthentication):
    def authenticate(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION',None)
        if auth is None:
            return  None

        auth_list = auth.split()
        #  校验合法还是非法用户
        if not (len(auth_list) == 2 and auth_list[0].lower() == 'auth'):
            raise AuthenticationFailed('非法用户')

        if auth_list[1] != 'abc.123.xyz':
            raise  AuthenticationFailed('用户校验失败')

        user = User.objects.filter(username='admin').first()
        if not user:
            raise AuthenticationFailed('用户数据有误,非法用户')

        return (user,None)
