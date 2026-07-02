from django.http import HttpResponse, JsonResponse , FileResponse
from django.shortcuts import render
from django.conf import settings

def info(request):
    data = {}
    print(request.META)
    # FileResponse("mysite-2027/mysite2026/urls.py")
    
    for k,v in request.headers.items():
        data[k] = v
        print(f"{k}: {v}")
    return JsonResponse(data)
def lucsood_pdf(request):
    file_path = settings.BASE_DIR / 'ลักหลับ.pdf'
    return FileResponse(
        open(file_path, 'rb'),
        content_type='application/pdf',
        filename='ลักหลับ.pdf'
    )

def shopping(request):
    return render(request, "shopping.html")

def home(request):
    return render(request, "index.html")

def old_home(request):
    return render(request, "home.html")
