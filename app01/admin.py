from django.contrib import admin
from .models import t_author
# Register your models here.

@admin.register(t_author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('f_id', 'f_name', )

