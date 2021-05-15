from django.urls import path,include
from . import views
import notifications.urls
urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('email_otp', views.email_otp, name='email_otp'),
    path('reset_password', views.reset_password, name='reset_password'),
    path('otp', views.otp, name='otp'),
    path('generateotp', views.generateotp, name='generateotp'),
    path('resend_otp', views.resend_otp, name='resend_otp'),
    path('profile', views.profile, name='profile'),
    path('user_edit', views.user_edit, name='user_edit'),
    path('basic_edit', views.basic_edit, name='basic_edit'),
    path('change_password', views.change_password, name='change_password'),
    path('reward', views.reward, name="reward"),
    path('user_request', views.user_request, name="user_request"),
    path('your_request', views.your_request, name="your_request"),
    path('delete', views.delete, name="delete"),

    path('noti', views.noti, name="noti"),
    path('mark', views.mark, name="mark"),
    path('remove', views.remove, name="remove"),
    path('removeAll', views.removeAll, name="removeAll"),
    path('markAll', views.markAll, name="markAll"),
    path('sendNotify', views.sendNotify, name="sendNotify"),
    path('notifications/', include(notifications.urls, namespace='notifications')),



    path('Food', views.Food, name='Food'),
    path('Clothes', views.Clothes, name='Clothes'),
    path('Books', views.Books, name='Books'),
    path('charity', views.charity, name='charity'),
    path('donation', views.donation, name='donation'),
    ]