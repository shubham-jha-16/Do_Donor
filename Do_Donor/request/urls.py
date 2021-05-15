from django.urls import path
from . import views
urlpatterns = [

     path('user_request', views.user_request, name="user_request"),
     path('ask_ngo', views.ask_ngo, name="ask_ngo"),
     path('request_donor', views.request_donor, name="request_donor"),
     path('your_request', views.your_request, name="your_request"),
     path('remove', views.remove, name="remove"),
    ]