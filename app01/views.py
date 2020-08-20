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
from rest_framework.filters import SearchFilter #过滤器
from rest_framework.pagination import PageNumberPagination
#   三大认证
from rest_framework.authentication import TokenAuthentication   #
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import SimpleRateThrottle
from rest_framework.parsers import JSONParser,FormParser,MultiPartParser
from rest_framework.generics import GenericAPIView
from rest_framework import exceptions
from utils.apiresponse import ApiResponse


def add_book(request):
    if request.method == "POST":
        print('add')
        new_book_name = request.POST['book_name']
        new_book_description = request.POST['book_description']
        new_book_country = request.POST['book_country']
        publisher_id = request.POST.get('publisher')
        # pub_obj=models.publisher_list.objects.get(publisher_id=publisher_id)
        models.Book_list.objects.create(book_name=new_book_name, book_country=new_book_country,
                                     book_description=new_book_description,book_publish_id=publisher_id)
        return redirect('/book_list/')
    all_pub_obj=models.publisher_list.objects.all()
    return render(request, 'add_book.html',{"all_pub_obj":all_pub_obj})

def remove_book(request):
    print('delete')
    print(request.GET)
    del_book_id=request.GET.get('id',None)
    if  del_book_id:
        models.Book_list.objects.get(book_id=del_book_id).delete()
    else:
        print('没有找到删除的id')
    return redirect('/book_list/')

def edit_book(request):
    if request.method == 'POST':
        edit_book_id=request.POST.get('book_id')
        print(request.POST)
        book_obj = models.Book_list.objects.get(book_id=edit_book_id)
        book_obj.book_name=request.POST.get('book_name')
        book_obj.book_description=request.POST.get('book_description')
        book_obj.book_country=request.POST.get('book_country')
        book_obj.book_publish_id = request.POST.get('publisher')
        book_obj.save()
        return redirect('/book_list/')
    edit_book_id=request.GET.get('id',None)
    all_publisher_obj = models.t_publisher.objects.all()
    if edit_book_id:
        book_obj=models.t_book.objects.get(book_id=edit_book_id)
        print(edit_book_id)
        return render(request,'edit_book.html',{'book_obj':book_obj,'all_publisher_obj':all_publisher_obj})
    else:
        return HttpResponse('ERROR edit_book_id')


class AddPublisher(View):
    def get(self,request):
        print(request.path_info)
        return render(request, 'add_publisher.html')
    def post(self,request):
        print(request.body)
        if request.method == "POST":
            publisher_name = request.POST.get("publisher_name")
            models.t_publisher.objects.create(publisher_name=publisher_name)
            return redirect('/publisher_list/')

def remove_publisher(request,publisher_id):
    print(type(publisher_id),publisher_id)
    models.t_publisher.objects.get(publisher_id=publisher_id).delete()
    return redirect('/publisher_list/')

def edit_publisher(request):
    if request.method == "POST":
        publisher_id = request.POST.get('publisher_id')
        publisher_name = request.POST.get('publisher_name')
        publisher_obj = models.t_publisher.objects.get(publisher_id=publisher_id)
        publisher_obj.publisher_name = publisher_name
        publisher_obj.save()
        return redirect('/publisher_list/')
    else:
        publisher_id=request.GET.get('id',None)
        num=request.GET.get('num',None)
        publisher_obj=models.t_publisher.objects.get(publisher_id=publisher_id)
        return render(request,'edit_publisher.html',{'publisher_obj':publisher_obj,'num':num})

def author_list(request):
    all_author_obj = models.t_author.objects.all()
    # author_obj_1 = all_author_obj[0]
    #author_ojb.book是什么,是把作者对应数据库里面book_list表中的两条记录给你
    # print(author_obj_1.book.all()[0].book_publish_id)
    # for author_obj in author_obj_1.book.all():
    #     print(author_obj.book_name)
    return render(request,'author_list.html',{'all_author_obj':all_author_obj})


def add_author(request):
    if request.method == 'POST':
        new_author_name = request.POST.get('author')
        books = request.POST.getlist('books')
        print(new_author_name,books)
        author_obj=models.t_author.objects.create(name=new_author_name)
        author_obj.book.set(books)
        return  redirect('/author_list/')
    all_book_obj = models.t_book.objects.all()
    return render(request,'add_author.html',{'all_book_obj':all_book_obj})

def remove_author(request):
    del_id=request.GET.get('id')
    models.Author.objects.get(id=del_id).delete()
    return redirect('/author_list/')

def edit_author(request):
    if request.method == 'POST':
        author_id = request.POST.get('author_id')
        author_name = request.POST.get('author')
        books = request.POST.getlist('books')
        print(author_id,author_name,books)
        author_obj = models.Author.objects.get(id=author_id)
        author_obj.name = author_name
        author_obj.book.set(books)
        author_obj.save()
        return redirect('/author_list/')
    edit_id = request.GET.get('id')
    author_obj = models.Author.objects.get(id=edit_id)
    all_book_obj = models.Book_list.objects.all()
    return render(request,'edit_author.html',{'author_obj':author_obj,'all_book_obj':all_book_obj})


def upload(request):
    if request.method == 'POST':
        filename = request.FILES["upload_file"].name
        with open(filename,'wb') as f:
            for chunk in request.FILES["upload_file"].chunks():
                f.write(chunk)
        return HttpResponse('上传ok')
    else:
        return  render(request,'upload.html')
def download(request):
    if request.method == 'POST':
        download_path=request.POST.get('download_path')
        hostname=request.POST.get('hostname')
        env=request.POST.get('env')
        os.chdir('/data/devops/ansible/deployments')
        cmd_ansible = "ansible -i ../inventories/%s/internal_hosts %s -m fetch -a 'src=%s  dest=/data/'"%(env,hostname,download_path)
        return HttpResponse(cmd_ansible)
    return render(request,'download.html')

def json_test(request):
    return render(request,'json_test.html')

def index(request):
    redirect_url = reverse('json_test')
    return redirect(redirect_url)

def transfer(request):
    if request.method == 'POST':
        return HttpResponse('转账成功')
    return render(request,'transfer.html')


class User(APIView):
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


class Publisher(GenericAPIView):
    queryset = models.t_publisher.objects.all()
    serializer_class = serializers.PublisherSerializer

    def get(self,request,*args,**kwargs):
        publisher_query = self.get_object()
        publisher_serialize = self.get_serializer(publisher_query)
        return  ApiResponse(results=publisher_serialize.data)

    def list(self,request,*args,**kwargs):
        publisher_query = self.get_queryset()
        publisher_serialize = self.get_serializer(publisher_query,many=True)
        return  ApiResponse(results=publisher_serialize.data)
