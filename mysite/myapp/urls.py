from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePage, name='home'),
    path('', views.DataDisplay, name = 'datadisplay'),
    path('', views.about_us, name = 'about_us')
]