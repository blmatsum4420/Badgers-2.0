from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def HomePage(request):
    # return render(request, 'HomePage.html', {})
    #return HttpResponse("Goodbye, world. You're dead")
    image_data = open("images/gary-may-trek.jpg", "rb").read()
    return HttpResponse(image_data, content_type="image/jpg")
def about_us(request):
    return render(request, 'about_us.html')

def DataDisplay(request):
    return render(request, 'data_display.html')

