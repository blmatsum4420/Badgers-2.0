from django.shortcuts import render
from django.http import HttpResponse
import weather_models
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
def changeImage(request):
    print(request.body)
    body = request.body.decode('ascii').split('&')
    print(body)
    body_dict = {}
    for pair in body:
        key, value = pair.split('=')
        body_dict[key] = value
    end = int(body_dict['end'])
    start = int(body_dict['start'])
    feature = body_dict['feature'].replace("+"," ")
    print(end, start, feature)

    weather_models.run_model(feature, end, start)
    return render(request, 'index.html', {})

