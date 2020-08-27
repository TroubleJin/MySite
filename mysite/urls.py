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
from rest_framework_jwt.views import ObtainJSONWebToken

urlpatterns = [
    path('admin/', admin.site.urls),
    # 单查群接口
    path(r'books/', views.Book.as_view()),
    path(r'books/<pk>/', views.Book.as_view()),
    # 单查群接口
    path(r'publishers/', views.Publisher.as_view()),
    path(r'publishers/<pk>/', views.Publisher.as_view()),
    path(r'user/', views.User.as_view()),
    # 单查群接口
    path(r'user/<pk>/', views.User.as_view()),
    path(r'sms/', views.Sms.as_view()),
    path(r'token/', ObtainJSONWebToken.as_view()),
    path(r'login/', views.LoginApiView.as_view()),
    path(r'school/', views.School.as_view()),
    path(r'school/<pk>/', views.School.as_view()),
]
