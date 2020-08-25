#!/usr/bin/env python
# coding=utf-8

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
import re
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserModelSerializer(ModelSerializer):
    # 自定义反序列化字段
    name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model =  User
        fields = ('name','password','username','email')
        extra_kwargs = {
            'email': {
                'read_only': True,
            },
            'username': {
                'read_only': True,
            },
            'password':{'write_only': True},
        }
    def validate(self, attrs):
        name = attrs.get('name')
        password = attrs.get('password')
        if re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$',name):
            user_obj= User.objects.filter(email=name).first()
        else:
            user_obj = User.objects.filter(username=name).first()
        if user_obj and user_obj.check_password(password):
            # 签发token
            payload = jwt_payload_handler(user_obj)
            self.token = jwt_encode_handler(payload)
            self.user_obj = user_obj
            return attrs
        raise serializers.ValidationError('数据有误')