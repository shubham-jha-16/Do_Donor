from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.models import auth,User
from account.models import User
from ngo.models import ngodata
from django.contrib import messages
from .models import requests,can,belongs_to
import datetime
from notifications.models import Notification
from notifications.signals import notify

# Create your views here.

# user send request to ngos
def user_request(request):
     if request.method == 'POST' :
         sector = request.POST['sector']
         location = request.POST['location']
         message = request.POST['message']
         date = datetime.date.today()

         req = requests(sector=sector, location=location, message= message, date=date)
         req.save();
         c = can(request_id=req.id, user_id=request.user.id)
         c.save();
         messages.info(request, 'your request has been sent to our NGOs')
         description = {"Requirement of" : sector,  "location" : location,  "message": message}
         print(description)
         user = User.objects.exclude(type='donor').exclude(id=request.user.id)
         notify.send(request.user, recipient=user, actor=request.user, verb='Request from donor for '+ sector ,
                     description= description,request_id= req.id )

         return redirect("/")












# user send request to ngos
def ask_ngo(request):
    if request.method == 'POST':
        sector = request.POST['sector']
        location = request.POST['location']
        message = request.POST['msg']
        date = datetime.date.today()

        u = requests(sector=sector, location=location, message=message, date=date, verified=True)
        u.save();
        rid = u.id
        c = belongs_to(request_id=rid, ngo_id=request.user.id, request_to='ngo')
        c.save()
        messages.info(request, 'Notification sent successfully to all NGOs')
        user = User.objects.exclude(type='donor').exclude(id=request.user.id)
        notify.send(request.user, recipient=user, actor=request.user, verb='Request from NGO for '+ sector , request_id=rid)

        return redirect("ngopannel")

    else:

        return render(request, "ngo_request.html")



def request_donor(request):
    if request.method == 'POST':
        sector = request.POST['sector']
        location = request.POST['location']
        message = request.POST['msg']
        date = datetime.date.today()

        u = requests(sector=sector, location=location, message=message, date=date, verified = True)
        u.save();
        rid = u.id
        c = belongs_to(request_id=rid, ngo_id=request.user.id, request_to='donors')
        c.save()
        messages.info(request, 'Notification sent successfully to all users')
        user = User.objects.exclude(type='ngo').exclude(id=request.user.id)
        notify.send(request.user, recipient=user, actor=request.user, verb='Request from NGO for '+ sector , request_id=rid)

        return redirect("ngopannel")

    else:
        return render(request, "ngo_request.html")



def your_request(request):

    if request.user.type=='donor':
        r = can.objects.filter(user_id=request.user.id).values_list('request_id')
        print(r)
        u = requests.objects.filter(id__in=r).order_by('-date')
        print(u)
        return render(request, "your_requests.html", {'request': u})
    if request.user.type == 'ngo':
        r = belongs_to.objects.filter(ngo_id=request.user.id).values_list('request_id')
        print(r)
        u = requests.objects.filter(id__in=r).order_by('-date')
        print(u)
        return render(request, "your_requests.html", {'request': u})

def delete(request):
    id = request.POST['id']

    requests.objects.filter(id=id).delete()
    Notification.objects.filter(request_id=id).delete()
    return your_request(request)