from asgiref import current_thread_executor
from django.contrib import admin
from django.urls import path
from mysite2026.view import *

urlpatterns = [
    path('lucsood/', lucsood_pdf),

    path('', old_home),
    path('solo/', home),
    path('shopping/', shopping),
    path('info/', info),
    path('admin/', admin.site.urls),
]
