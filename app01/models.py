from django.db import models

# Create your models here.

class UserInfo(models.Model):
    id = models.AutoField(primary_key=True)               #创建一个自增主键
    name = models.CharField(null=False,max_length=20)     #创建一个VARCHAR类型不能为空的字段
    password = models.CharField(null=False,max_length=20)

class Book_list(models.Model):
    book_id = models.AutoField(primary_key=True)
    book_name = models.CharField(null=True,max_length=64)
    book_description = models.CharField(null=True,max_length=64)
    book_country = models.CharField(null=True,max_length=64)