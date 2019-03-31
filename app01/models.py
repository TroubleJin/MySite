from django.db import models

# Create your models here.

class publisher_list(models.Model):
    publisher_id = models.AutoField(primary_key=True)
    publisher_name = models.CharField(null=True,max_length=64)

class Book_list(models.Model):
    book_id = models.AutoField(primary_key=True)
    book_name = models.CharField(null=True,max_length=64)
    book_description = models.CharField(null=True,max_length=64)
    book_country = models.CharField(null=True,max_length=64)
    book_publish = models.ForeignKey(publisher_list,to_field='publisher_id',on_delete='CASCADE')

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16,null=False,unique=True)
    book = models.ManyToManyField(Book_list)