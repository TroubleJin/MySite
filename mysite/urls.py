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
from django.urls import path
from app01 import views

urlpatterns = [
    path('book_list/', views.book_list),
    # path('add_book/', add_book),
    # path('remove_book/', remove_book),
    # path('edit_book/', edit_book),
    path('admin/', admin.site.urls),
    path('publisher_list/', views.publisher_list),
    path('add_publisher/', views.add_publisher),
    path('remove_publisher/', views.remove_publisher),
    path('edit_publisher/', views.edit_publisher),
]
