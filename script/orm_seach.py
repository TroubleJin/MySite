import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
from app01 import models
# 查询所有
# ret = models.Book_list.objects.all()
# print(ret)
#
# #  排除查询
# ret = models.Book_list.objects.exclude(book_id=1)
# print(ret)
#
# #  查询字段的值
# ret = models.Book_list.objects.values("book_name")
# print(ret)
#
# #   根据什么排序
# ret = models.Book_list.objects.order_by('book_name')
# print(ret)
#
# # 查询次数
# ret = models.Book_list.objects.all().count()
# print(ret)

# 外键的正向查询
# 基于对象查询
# book_obj = models.Book_list.objects.all().first()
# ret = book_obj.book_publish.publisher_name
# print(ret)
# # 双下划线表示库跨表查询
# ret =models.Book_list.objects.filter(book_id=1).values_list('book_publish__publisher_name')
# print(ret)
#
# #   外键的反向查询
# publisher_obj = models.publisher_list.objects.first()
# ret = publisher_obj.book_list_set.all()
# print(ret)
#
# print(models.publisher_list.objects.filter(book_list__author__id=1).values('book_list__book_name'))


# author_obj = models.Author.objects.first()
# 查询所有书籍
# print(author_obj.book.all())
# 创建create
# author_obj.book.create(book_name='大家好',book_description='大家好',book_country='大家好',
#                        book_publish_id=1)

#  添加关联关系add
# book_obj = models.Book_list.objects.get(book_id=5)
# author_obj.book.add(book_obj)
#
#   添加多个关系
# books_obj = models.Book_list.objects.filter(book_id__gt = 1)
# author_obj.book.add(*books_obj)

# pub_obj  = models.publisher_list.objects.get(publisher_id=1)
# print(pub_obj.book_list_set.filter(book_id__gt=0))

# 聚合
# from django.db.models import Avg,Count,Sum,Q,F
# ret = models.t_book.objects.all().aggregate(Avg('book_price'))
# print(ret)
#
#
# #   分组查询
# ret = models.t_book.objects.all()
# for i in ret:
#     print(i.book_name,i.author_set.values("name"))
#
# #  查询每一本书的作者的数量
# ret = models.t_book.objects.all().annotate(author_num = Count('author'))
# for book in ret :
#     print(book.book_name,book.author_num)
#
# #   查询作者数量大于一的书籍
# ret = models.t_book.objects.all().annotate(author_num = Count('author')).filter(author_num__gt=1)
# for book in ret :
#     print(book.book_name,book.author_num)
#
# #   查询各个作者出的书总价格
# ret = models.t_author.objects.all().annotate(price_num = Sum('book__book_price')).values_list('name','price_num')
# print(ret)

##

from django.contrib.auth.models import User,Group,Permission

user = User.objects.first()
print(user.username)
print(user.groups.first())

group = Group.objects.first()
print(group.name)
print(group.user_set.first())

