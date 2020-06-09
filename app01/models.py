from django.db import models

# Create your models here.

class t_publisher(models.Model):
    f_id = models.AutoField(verbose_name=u"出版社id",primary_key=True)
    f_publisher_name = models.CharField(verbose_name=u"出版社名称",null=True,max_length=64)
    class Meta:
        db_table = 't_publisher'

class t_book(models.Model):
    f_id = models.AutoField(verbose_name=u"书籍id",primary_key=True)
    f_book_name = models.CharField(verbose_name=u"书籍名称",null=True,max_length=64)
    f_book_description = models.CharField(verbose_name=u"书籍描述",null=True,max_length=64)
    f_book_country = models.CharField(verbose_name=u"书籍国家",null=True,max_length=64)
    f_book_price = models.IntegerField(verbose_name=u"书籍价格",null=True,default=99)
    f_book_publish = models.ForeignKey(t_publisher,to_field='f_id',on_delete='CASCADE')
    class Meta:
        db_table = 't_book'

class t_author(models.Model):
    f_id = models.AutoField(verbose_name=u"作者id",primary_key=True)
    f_name = models.CharField(verbose_name=u"作者姓名",max_length=16,null=False,unique=True)
    f_book = models.ManyToManyField(t_book)
    class Meta:
        db_table = 't_author'
