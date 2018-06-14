"""mss_rili URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from hello import views as hello_views  # new

import hello.views as bv

urlpatterns = [
    path('', hello_views.index),  # new
    path('demo', hello_views.demo),  # new
    path('admin', admin.site.urls),
    path('rili', hello_views.rili,name='rili'),
    # 注意这里对应我view层里面的home函数
    #url(r'^$', bv.sousuo),
    path('sousuo',bv.sousuo),
    path('test',bv.test),
    path('dao',bv.dao),
]
