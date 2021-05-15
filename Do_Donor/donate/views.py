from django.shortcuts import render
from .models import Destination
from account.models import User
from request.models import requests
from donation.models import donation_data
from ngo.models import ngodata
from django.db.models import Sum
#from django.db.models import
# Create your views here.

def index(request):
     dests = Destination.objects.all()
     news=requests.objects.all().order_by('-date')[:4]
     amount=donation_data.objects.all().aggregate(Sum('amount'))
     books = donation_data.objects.filter(sector="Books").aggregate(Sum('quantity'))
     clothes = donation_data.objects.filter(sector="Clothes").aggregate(Sum('quantity'))
     food = donation_data.objects.filter(sector="Food").aggregate(Sum('quantity'))
     ngo= ngodata.objects.count()
     print(amount["amount__sum"])
     print(books["quantity__sum"])
     print(clothes["quantity__sum"])
     print(food["quantity__sum"])
     print(ngo)
     print(news)
     return render(request, "home.html", {'dests': dests,'news': news, 'amount': amount["amount__sum"],'books': books["quantity__sum"],'clothes': clothes["quantity__sum"],'food': food["quantity__sum"], 'ngo': ngo})


def about_ngo(request):
     dests = User.objects.filter(type='ngo')
     return render(request, "about_ngo.html", {'dests': dests})


def contact(request):
     return render(request, "contact us.html")