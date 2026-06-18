"""
URL configuration for mysite2026 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from asgiref import current_thread_executor
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path
from django.shortcuts import render

def info(request):
    ip_address = request.META['REMOTE_ADDR']
    res_txt = f"Your IP Address is {ip_address}\n"
    
    for k,v in request.headers.items():
        res_txt += f"<p> {k}:{v}<p>\n"
    return HttpResponse(res_txt)

def home(request):
    return render(request, "index.html")

def old_home(request):
    return render(request, "home.html")

urlpatterns = [
    path('', old_home),
    path('solo/', home),
    path('info/', info),
    path('admin/', admin.site.urls),
]
