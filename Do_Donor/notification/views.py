from django.core import serializers
from django.template import RequestContext
from django.shortcuts import render, redirect,HttpResponse
from notifications.models import Notification
from notifications.signals import notify
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib import messages
from account.models import User
from request.models import requests,can,belongs_to
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_protect

def noti(request):

    lists = []
    print(request.user.notifications.all())

    for i in request.user.notifications.unread():
        lists.append(i)

    list1 = []
    for i in request.user.notifications.read():
        list1.append(i)

    return render(request, "notification.html", {'notice': lists, 'read': list1})


def sendNotify(request):
    user = User.objects.all()

    notify.send(request.user, recipient=user, actor=request.user, verb='you have reached level 1', )
    return HttpResponse("Notification sent successfully!")

@csrf_protect
def mark(request):
    noti = request.GET['noti']
    noti = Notification.objects.get(id=noti)
    noti.mark_as_read()
    request_id= noti.request_id
    print(request_id)
    data= requests.objects.get(id=request_id)
    c = 0
    if can.objects.filter(request_id=request_id).values_list('user_id'):
        c = can.objects.filter(request_id=request_id).values_list('user_id')
    else:
        c = belongs_to.objects.filter(request_id=request_id).values_list('ngo_id')
        request.session['ngo_id'] = User.objects.get(id=c[0][0]).id
        context = RequestContext(request)
        context['ngo_id'] = request.session['ngo_id']
    user = User.objects.get(id=c[0][0])

    return render(request, "message.html", {'noti': noti, 'data': data, 'u': user })




def markAll(request):
    request.user.notifications.mark_all_as_read(request.user)
    return HttpResponse("success")


def remove(request):
    noti = request.POST.get('noti')
    print(noti)
    noti = Notification.objects.get(id=noti)
    noti.deleted = True
    noti.save()
    return HttpResponse(noti)


def removeAll(request):
    request.user.notifications.mark_all_as_deleted(request.user)
    return HttpResponse("success")


def interest(request):
    if request.method == 'POST':
        interest = request.POST['interest']
        ngo_id = int(request.POST['me'])
        r_id = int(request.POST['reciever'])
        if interest == 'Yes' :


            ngo = User.objects.get(id=ngo_id)
            c=0
            if  can.objects.filter(request_id=r_id).values_list('user_id') :
                c= can.objects.filter(request_id=r_id).values_list('user_id')
            else:
                c = belongs_to.objects.filter(request_id=r_id).values_list('ngo_id')
            user = User.objects.get(id=c[0][0])

            message = ngo.ngodata.ngo_name +'will fulfill your request after verification'
            send_mail(
            'Do Donor.com ',
            message,
            settings.EMAIL_HOST_USER,
            [user.email], fail_silently=False)
            Notification.objects.filter(request_id=r_id).exclude(recipient_id=ngo_id).delete()
            print('notification deleted')
            messages.info(request, 'Thankyou!! please verify the request before donating (if request status shown to you is not verified) ')
            return redirect('ngopannel')
        else:
            Notification.objects.filter(request_id=r_id, recipient_id=ngo_id).delete()
            print('notification deleted')
            return redirect(noti)