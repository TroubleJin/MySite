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
    path('add_book/', views.add_book),
    path('remove_book/', views.remove_book),
    path('edit_book/', views.edit_book),
    path('admin/', admin.site.urls),
    path('publisher_list/', views.publisher_list),
    path('add_publisher/', views.AddPublisher.as_view()),
    path('remove_publisher/', views.remove_publisher),
    path('edit_publisher/', views.edit_publisher),
    path('author_list/', views.author_list),
    path('add_author/', views.add_author),
    path('remove_author/', views.remove_author),
    path('edit_author/', views.edit_author),
    path('upload/', views.upload),
    path('download/', views.download),
]
