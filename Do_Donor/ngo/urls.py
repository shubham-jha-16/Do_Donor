from django.urls import path, include
from . import views
import notifications.urls
urlpatterns = [
    path('ngo', views.ngo, name='ngo'),
    path('nlogin', views.nlogin, name='nlogin'),
    path('ngopannel', views.ngopannel, name='ngopannel'),
    path('nlogout', views.nlogout, name='nlogout'),
    path('notp', views.notp, name='notp'),
    path('resendotp', views.resendotp, name='resendotp'),
    path('generate_otp', views.generate_otp, name='generate_otp'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('email_otp', views.email_otp, name='email_otp'),
    path('reset_password', views.reset_password, name='reset_password'),
    path('ngo_edit', views.ngo_edit, name='ngo_edit'),
    path('basic_edit', views.basic_edit, name='basic_edit'),
    path('change_password', views.change_password, name='change_password'),
    path('ngo_request', views.ngo_request, name='ngo_request'),
    path('ask_ngo', views.ask_ngo, name="ask_ngo"),
    path('request_donor', views.request_donor, name="request_donor"),
    path('your_request', views.your_request, name="your_request"),
    path('delete', views.delete, name="delete"),

    path('noti', views.noti, name="noti"),
    path('mark', views.mark, name="mark"),
    path('remove', views.remove, name="remove"),
    path('removeAll', views.removeAll, name="removeAll"),
    path('markAll', views.markAll, name="markAll"),
    path('sendNotify', views.sendNotify, name="sendNotify"),
    path('notifications/', include(notifications.urls, namespace='notifications')),


    path('interest', views.interest, name="interest"),


]
