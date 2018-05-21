# coding:utf-8
from django.core.management import templates
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

#这里对应html文件
def sousuo(request):
    return render(request, 'test.html')
def dao(request):
    return render(request, 'leftnav.html')
def test1(request):
    return render(request, 'test1.html')

def demo(request):
    return HttpResponse(u"欢迎光临，自强学堂!这是一个demo！")

def index(request):
    return HttpResponse(u"这是一个登录界面!！")

def rili(request):
    yy = request.GET['yy']
    mm = request.GET['mm']
    dd = request.GET['dd']
    return HttpResponse("这是日期：%s/%s/%s"%(yy,mm,dd))