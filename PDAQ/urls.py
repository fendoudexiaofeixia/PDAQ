"""PDAQ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
import xadmin
from django.contrib import admin
from django.urls import path, re_path
from my_app.views import pdaq_list, pdaq_detail

urlpatterns = [
    path('admin/', xadmin.site.urls),
    re_path(r'^$', pdaq_list,name='pdaq_list'),
    re_path(r'^category/(?P<category_id>\d+)/$', pdaq_list, name='category_list'),
    re_path(r'^custom/(?P<custom_id>\d+)/$', pdaq_list, name='custom_list'),
    re_path(r'^pdaq/(?P<serial_number>\d+).html$', pdaq_detail, name='serial_list'),
]
