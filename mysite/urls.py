"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from app01 import views


urlpatterns = [
    path(r'books/', views.Book.as_view()),
    # 单查群接口
    path(r'books/<pk>/', views.Book.as_view()),
    path(r'publishers/', views.Publisher.as_view()),
    # 单查群接口
    path(r'publishers/<pk>/', views.Publisher.as_view()),
    re_path('add_book/', views.add_book),
    path('remove_book/', views.remove_book),
    path('edit_book/', views.edit_book),
    path('admin/', admin.site.urls),
    path('add_publisher/', views.AddPublisher.as_view()),
    path(r'remove_publisher/page<publisher_id>', views.remove_publisher),
    path('edit_publisher/', views.edit_publisher),
    path('author_list/', views.author_list),
    path('add_author/', views.add_author),
    path('remove_author/', views.remove_author),
    path('edit_author/', views.edit_author),
    path('upload/', views.upload),
    path('download/', views.download),
    path('json_test111/', views.json_test,name='json_test'),
    path('index/', views.index),
    path('transfer/', views.transfer),
    path(r'user/', views.User.as_view()),
    # 单查群接口
    path(r'user/<pk>/', views.User.as_view()),
]
