from django.contrib import admin
from .models import t_author
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




