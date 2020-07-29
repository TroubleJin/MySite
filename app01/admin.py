from django.contrib import admin
from .models import t_author,t_book,t_publisher
# Register your models here.

@admin.register(t_author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('f_id', 'f_name', )
    actions_on_top = True
    filter_horizontal = ['f_book']
    # 可以使用跨表查询,右侧出现选择
    list_filter = ('f_book__f_book_name', )
    #   顶部出现搜索框
    search_fields = ['f_name']


@admin.register(t_publisher)
class PublisherrAdmin(admin.ModelAdmin):
    list_display = ('f_id', 'f_publisher_name', )
    actions_on_top = True
    #   顶部出现搜索框
    search_fields = ['f_publisher_name']

@admin.register(t_book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('f_id', 'f_book_name', 'f_book_description','f_book_country','f_book_price','f_book_publish')
    actions_on_top = True
    #   顶部出现搜索框
    search_fields = ['f_book_name']






