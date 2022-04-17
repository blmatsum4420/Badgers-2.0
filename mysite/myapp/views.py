from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(request):
    return render(request, 'index.html', {})
    #return HttpResponse("Goodbye, world. You're dead")
    #image_data = open("images/gary-may-trek.jpg", "rb").read()
    #return HttpResponse(image_data, content_type="image/jpg")
def about_us(request):
    return HttpResponse("ABOUT US PAGE")
    #return render(request, 'about_us.html')

def data_display(request):
    #return HttpResponse("DATA DISPLAY PAGE")
    return render(request, 'data_display.html')

def empty(request):
    return render(request, 'index.html', {})

