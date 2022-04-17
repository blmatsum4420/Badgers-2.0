from django.urls import path

from . import views

urlpatterns = [
    path('home', views.home_page, name='home'),
    path('data_display', views.data_display, name = 'data_display'),
    path('about_us', views.about_us, name = 'about_us'),
    path('', views.empty, name = 'empty')
]