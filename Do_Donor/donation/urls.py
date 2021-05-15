from django.urls import path
from . import views
urlpatterns = [


    path('Food', views.Food, name='Food'),
    path('Clothes', views.Clothes, name='Clothes'),
    path('Books', views.Books, name='Books'),
    path('charity', views.charity, name='charity'),
    path('donation', views.donation, name='donation'),
]
