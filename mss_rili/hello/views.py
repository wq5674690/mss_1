from django.core.management import templates
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

#这里对应html文件
def sousuo(request):
    return render(request, 'test.html')