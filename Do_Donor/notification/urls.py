import notifications.urls
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.noti, name="noti"),
    path('mark', views.mark, name="mark"),
    path('remove', views.remove, name="remove"),
    path('removeAll', views.removeAll, name="removeAll"),
    path('markAll', views.markAll, name="markAll"),
    path('sendNotify', views.sendNotify, name="sendNotify"),
    path('notification/', include(notifications.urls, namespace='notifications')),

    path('interest', views.interest, name="interest"),
    ]