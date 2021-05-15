from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('about_ngo', views.about_ngo, name='about_ngo'),
    path('contact', views.contact, name='contact'),
]
