"""
URL configuration for mainproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from mainapp.views import login_view, logout_view, success_view, calculate_view, defult, calculate_page_index, calculate_detail, register_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view),
    path('calculate_page/',calculate_view, name='calculate_page'),
    path('calculate_page_index/',calculate_page_index, name='calculate_page_index/'),
    path('calculate_page_index/detail/', calculate_detail, name='calculate_page_index_detail/'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('success_page/',success_view, name='success_page'),
    path('defult/',defult, name='defult'),
]
