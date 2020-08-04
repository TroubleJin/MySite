from rest_framework import serializers
from rest_framework import exceptions
from . import models


class UserSerializer(serializers.Serializer):
    f_name = serializers.CharField()
    f_password = serializers.CharField()
    f_phone = serializers.CharField()
    f_sex = serializers.IntegerField()
    #  自定义序列化属性
    def get_gender(self,obj):
        return obj.get_f_sex_display()


class UserDeserializer(serializers.Serializer):
    f_name = serializers.CharField(
        max_length=10,min_length=2,error_messages={
            'max_length': '名称太长',
            'min_length': '名称太短'
        }
    )
    f_phone = serializers.CharField()
    f_password = serializers.CharField(max_length=32)
    f_sex = serializers.IntegerField()
    #  自定义有校验规则的反序列化字段
    re_f_password = serializers.CharField(max_length=32)

    #   字段级反序列化
    # def validate_f_name(self,value):
    #     if '0' in value.lower():
    #         raise exceptions.ValidationError('名字错误')
    #     return value
    #
    # def validate_f_password(self, value):
    #     if '0' in value.lower():
    #         raise exceptions.ValidationError('密码带0,不行')
    #     return value
    #
    # #   对象级验证
    # def validate(self, attrs):
    #     # 必须pop走,不能留下多余字段
    #     if attrs.get('f_password') != attrs.pop('re_f_password'):
    #         raise  exceptions.ValidationError('两次密码不一致')
    #     return attrs

    def create(self, validated_data):
        return models.t_user.objects.create(**validated_data)