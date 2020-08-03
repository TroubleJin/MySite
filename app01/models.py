from django.db import models

# Create your models here.

class t_publisher(models.Model):
    f_id = models.AutoField(verbose_name=u"出版社id",primary_key=True)
    f_publisher_name = models.CharField(verbose_name=u"出版社名称",null=True,max_length=64)
    class Meta:
        db_table = 't_publisher'
        verbose_name_plural = '出版社'

class t_book(models.Model):
    f_id = models.AutoField(verbose_name=u"书籍id",primary_key=True)
    f_book_name = models.CharField(verbose_name=u"书籍名称",null=True,max_length=64)
    f_book_description = models.CharField(verbose_name=u"书籍描述",null=True,max_length=64)
    f_book_country = models.CharField(verbose_name=u"书籍国家",null=True,max_length=64)
    f_book_price = models.IntegerField(verbose_name=u"书籍价格",null=True,default=99)
    f_book_publish = models.ForeignKey(t_publisher,to_field='f_id',on_delete='CASCADE')
    class Meta:
        db_table = 't_book'
        verbose_name_plural = '书籍'

class t_author(models.Model):
    f_id = models.AutoField(verbose_name=u"作者id",primary_key=True)
    f_name = models.CharField(verbose_name=u"作者姓名",max_length=16,null=False,unique=True)
    f_book = models.ManyToManyField(t_book)
    class Meta:
        db_table = 't_author'
        verbose_name_plural = '作者'


class t_user(models.Model):
    SEX_CHOICES = [
        [0,"男"],
        [1,"女"],
    ]
    f_id = models.AutoField(verbose_name='用户id',primary_key=True)
    f_name = models.CharField(verbose_name='用户名称',max_length=64)
    f_password = models.CharField(verbose_name='用户密码',max_length=32)
    f_phone = models.CharField(verbose_name='手机号',max_length=11)
    f_sex = models.IntegerField(choices=SEX_CHOICES,default=0)
    class Meta:
        db_table = 't_user'
        verbose_name_plural = '用户'

