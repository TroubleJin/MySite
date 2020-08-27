from django.shortcuts import render,redirect
# Create your views here.
from app01 import models
from django.urls import reverse
from django.http import HttpResponse,JsonResponse
from django.views import View
from . import serializers
import os
#   drf框架封装风格
from rest_framework.views import APIView
from rest_framework.response import  Response
from rest_framework.request import Request
from rest_framework.settings import APISettings
from rest_framework.pagination import PageNumberPagination
#   三大认证
from rest_framework.authentication import TokenAuthentication   #
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser
from rest_framework.throttling import SimpleRateThrottle
from rest_framework.parsers import JSONParser,FormParser,MultiPartParser
from rest_framework.generics import GenericAPIView,ListCreateAPIView,RetrieveUpdateAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import exceptions
from utils.apiresponse import ApiResponse
from .permissions import Permission
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework_jwt.serializers import jwt_encode_handler
from rest_framework.filters import OrderingFilter,SearchFilter
from rest_framework.permissions import IsAdminUser

class User(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JSONWebTokenAuthentication]
    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        if pk:
            user_obj = models.t_user.objects.get(f_id=pk)
            data = {
                'status': 0,
                'result': serializers.UserSerializer(user_obj).data
            }
        else:
           user_obj = models.t_user.objects.all()
           data = {
               'status': 0,
               'result': serializers.UserSerializer(user_obj,many=True).data
           }
        return Response(data=data)
    #   只考虑单增
    def post(self,request,*args,**kwargs):
        request_data = request.data
        if not isinstance(request_data,dict):
            return  Response({
                'status': 1,
                'result': '数据有误'
            })
        #   数据合法,但数据内容不一定合法
        user_serializes = serializers.UserDeserializer(data=request_data)
        user_serializes.is_valid(raise_exception=True)
        user_obj = user_serializes.save()
        return Response({
            'status': 0,
            'result': serializers.UserSerializer(user_obj).data
        })
        # else:
        #     return Response({
        #         'status': 1,
        #         'result':  user_serializes.errors
        #     })

class Book(APIView):
    # 单查群差
    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        if pk:
            book_obj = models.t_book.objects.get(pk=pk)
            many = False
        else:
            book_obj = models.t_book.objects.all()
            many = True
        return ApiResponse(results=serializers.BookSerializer(book_obj,many=many).data)

    # 单增群增
    def post(self,request,*args,**kwargs):
        request_data = request.data
        if isinstance(request_data,dict):
            many = False
        elif isinstance(request_data,list):
            many = True
        else:
            raise  exceptions.ValidationError('类型错误')
        book_serializers = serializers.BookSerializer(data=request_data,many=many)
        book_serializers.is_valid(raise_exception=True)
        book_obj = book_serializers.save()
        return ApiResponse(results=serializers.BookSerializer(book_obj))

    # 单群删除
    def delete(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        if pk:
            pks = [pk]
        else:
            pks = request.data.get('pks')
        if models.t_book.objects.filter(pk__in=pks).delete():
            return  Response('删除成功')
        return  Response('删除失败')

    #   单群体改
    def put(self,request,*args,**kwargs):
        request_data = request.data
        pk = kwargs.get('pk')
        old_book_obj = models.t_book.objects.filter(pk=pk).first()
        # partial设置是否校验所有字段
        book_serializers = serializers.BookSerializer(instance=old_book_obj,data=request_data,partial=True)
        book_serializers.is_valid(raise_exception=True)
        #   检验通过完成数据更新
        book_obj = book_serializers.save()
        return Response(serializers.BookSerializer(book_obj).data)

    #  单体部改
    def patch(self,request,*args,**kwargs):
        # request_data = request.data
        # pk = kwargs.get('pk')
        # pks = []
        # if not pk and isinstance(request_data,list): #群改
        #     for data in request_data:
        #         pk = data.get('pk')
        #         pks.append(pk)
        #         old_book_obj = models.t_book.objects.filter(pk=pk).first()
        #         book_serializers = serializers.BookSerializer(instance=old_book_obj,data=data,partial=True)
        #         book_serializers.is_valid(raise_exception=True)
        #         #   检验通过完成数据更新
        #         book_obj = book_serializers.save()
        #     book_objs = models.t_book.objects.filter(f_id__in=pks)
        #     return Response(serializers.BookSerializer(book_objs,many=True).data)
        # elif pk and isinstance(request_data,dict): #单改
        #     old_book_obj = models.t_book.objects.filter(pk=pk).first()
        #     book_serializers = serializers.BookSerializer(instance=old_book_obj, data=request_data, partial=True)
        #     book_serializers.is_valid(raise_exception=True)
        #     #   检验通过完成数据更新
        #     book_obj = book_serializers.save()
        #     return Response(serializers.BookSerializer(book_obj).data)
        # else:
        #     return Response('数据有误')



        request_data = request.data
        pk = kwargs.get('pk')

        # 将单改，群改的数据都格式化成 pks=[要需要的对象主键标识] | request_data=[每个要修改的对象对应的修改数据]
        if pk and isinstance(request_data, dict):  # 单改
            pks = [pk, ]
            request_data = [request_data, ]
        elif not pk and isinstance(request_data, list):  # 群改
            pks = []
            for dic in request_data:  # 遍历前台数据[{pk:1, name:123}, {pk:3, price:7}, {pk:7, publish:2}]，拿一个个字典
                pk = dic.pop('pk', None)
                if pk:
                    pks.append(pk)
                else:
                    return Response({
                        'status': 1,
                        'msg': '数据有误',
                    })
        else:
            return Response({
                'status': 1,
                'msg': '数据有误',
            })
        # pks与request_data数据筛选，
        # 1）将pks中的没有对应数据的pk与数据已删除的pk移除，request_data对应索引位上的数据也移除
        # 2）将合理的pks转换为 objs
        objs = []
        new_request_data = []
        for index, pk in enumerate(pks):
            try:
                # pk对应的数据合理，将合理的对象存储
                obj = models.t_book.objects.get(f_id=pk)
                objs.append(obj)
                # 对应索引的数据就需要保存下来
                new_request_data.append(request_data[index])
            except:
                # 重点：反面教程 - pk对应的数据有误，将对应索引的data中request_data中移除
                # index = pks.index(pk)
                # request_data.pop(index)
                continue
        print(objs)
        print(new_request_data)
        book_ser = serializers.BookSerializer(instance=objs, data=new_request_data, partial=True, many=True)
        book_ser.is_valid(raise_exception=True)
        book_objs = book_ser.save()

        return Response({
            'status': 0,
            'msg': 'ok',
            'results': serializers.BookSerializer(book_objs, many=True).data
        })



class Publisher(ListCreateAPIView,RetrieveUpdateAPIView):
    queryset = models.t_publisher.objects.filter()
    serializer_class = serializers.PublisherSerializer
    permission_classes = [Permission]


from .throtties import SMSRateThrottle
class Sms(APIView):
    throttle_classes = [SMSRateThrottle]
    def get(self,request,*args,**kwargs):
        return ApiResponse(results='get 获取验证码ok')
    def post(self,request,*args,**kwargs):
        return ApiResponse(results='post 获取验证码Ok')

#   实现多方式登录签发token：账号、手机号、邮箱等登录
#   1.禁用认证与权限组件
#   2.拿到前台登录信息
#   3.校验得到登录用户
#   4.签发token并返回
from app02.serializers import UserModelSerializer
class LoginApiView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self,request,*args,**kwargs):
        request_data = request.data
        user_serializer = UserModelSerializer(data=request_data)
        user_serializer.is_valid(raise_exception=True)
        data = UserModelSerializer(user_serializer.user_obj).data
        return ApiResponse(results=data,token=user_serializer.token)


from .pagenations import Pagenation,OffsetPagination,CustomPagination
from .filters import LimitFilter
class School(RetrieveUpdateAPIView,ListCreateAPIView):
    queryset = models.t_school.objects.filter()
    serializer_class = serializers.SchoolSerializer
    # 局部配置过滤类
    filter_backends = [SearchFilter,OrderingFilter,LimitFilter]
    search_fields = ('f_name', 'f_region','f_price')
    ordering_fields = ['f_price']
    pagination_class = Pagenation
    def get(self,request,*args,**kwargs):
        if 'pk' in kwargs:
            results = self.retrieve(request,*args,**kwargs).data
        else:
            results =  self.list(request,*args,**kwargs).data
        return ApiResponse(results=results)
