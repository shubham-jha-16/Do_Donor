from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User,auth
from account.models import User
from ngo.models import ngodata
from .models import donation_data
from django.contrib import messages
import datetime
from request.models import requests, can, belongs_to
import random
from django.views.decorators.cache import cache_control
from django.core.mail import send_mail
from django.conf import settings



def donation(request):
    if request.method == "POST":
            sector = request.POST['sectors']
            NGO = request.POST['ngo']
            amount = request.POST['amount']
            print(sector + " " + NGO)
            if NGO=='None':
                if sector=='None':
                  r1= requests.objects.all()
                  r2=belongs_to.objects.filter(request_id__in=r1, request_to='donors').values_list('ngo_id')
                  if r2:
                      r3 = random.choices(r2)
                      ngo_id = r3[0][0]
                  else:
                      n1 = User.objects.filter(type='ngo')
                      n2 = random.choice(n1)
                      print(str(n2.id) + str(n2.ngodata.ngo_name))
                      print('case2')
                      print('ngo none sector none but no request')
                      ngo_id = n2.id
                else:
                    r1 = requests.objects.filter(sector__contains=sector)
                    if r1 is None:
                        n1 = User.objects.filter(type='ngo')
                        n2 = random.choices(n1)
                        print(n2.id + n2.ngodata.ngo_name)
                        print('case3')
                        print('ngo none sector selected but no request for sector')
                        ngo_id = n2.id

                    else:

                        r2 = belongs_to.objects.filter(request_id__in=r1, request_to='donors').values_list('ngo_id')
                        if r2:
                            print('id')
                            print(len(r2))
                            for x in range(len(r2)):
                                print(r2[x])
                            r3 = random.choices(r2)
                            print(r3[0][0])
                            ngo_id = r3[0][0]
                            print('case4')
                            print('ngo none sector selected')
                            print(str(ngo_id))
                        else:
                            n1 = User.objects.filter(type='ngo')
                            n2 = random.choice(n1)
                            print(str(n2.id) + str(n2.ngodata.ngo_name))
                            print('case5')
                            print('ngo none sector selected but no request')
                            ngo_id = n2.id
            else:
                 n = ngodata.objects.get(ngo_name=NGO)
                 ngo_id = n.user_id
                 print('case6')
                 print('sector selected/none ngo selected but no request')
            date = datetime.date.today()
            data = donation_data(donor_id=request.user.id, ngo_id=ngo_id, address=request.user.address, sector="charity", category=sector,
                                 amount=amount, mode="online", date=date)
            data.save()
            return redirect('/')



def charity(request):

    if request.method == "POST":
        sector = request.POST['sectors']
        print(sector)
        if sector =='None':
                ngo = ngodata.objects.all()
                print(ngo[0])
                address=User.objects.filter(id__in=ngo)
                print(address[0].address)

        else:
                ngo = ngodata.objects.filter(sector__contains=sector)
                if ngo:
                  print(len(ngo))
                  print(ngo[0])
                  address = User.objects.filter(id__in=ngo)
        a = "["
        b = "["
        for i in range(0, len(ngo) - 1):
            a = a + '"' + ngo[i].ngo_name + '",'
            b = b + '"' + address[i].address + '",'
        a = a + '"' + ngo[len(ngo) - 1].ngo_name + '"' + "]"
        b = b + '"' + address[len(ngo) - 1].address + '"' + "]"

        print(a+""+b)
        json= '{"name": ' +a+ ', "address": ' +b+ '}'
        print(json)
        return HttpResponse(json)
    else:

        u = User.objects.get(username=request.user.username)
        n= ngodata.objects.all()

        return render(request, "charity.html", {'user': u, 'ngo': n})


# food donation
def Food(request):
    if request.method == 'POST':
        email = request.POST['email']
        address = request.POST['address']
        sector = request.POST['sector']
        category = request.POST['category']
        ngo = request.POST['ngo']
        quantity = request.POST['quantity']
        if ngo=='none':
            r1=requests.objects.filter(sector__contains='Food')

            if r1 is None :
                n1=User.objects.filter(type='ngo')
                n2=random.choices(n1)
                print(n2.id + n2.ngodata.ngo_name)
                ngo_id=n2.id
            else:

                r2=belongs_to.objects.filter(request_id__in=r1, request_to='donors').values_list('ngo_id')
                if r2  :
                    print('id')
                    print(len(r2))
                    for x in range(len(r2)):
                        print(r2[x])
                    r3= random.choices(r2)
                    print(r3[0][0])
                    ngo_id= r3[0][0]
                    print(str(ngo_id))
                else:
                    n1 = User.objects.filter(type='ngo')
                    n2 = random.choice(n1)
                    print(str(n2.id) + str(n2.ngodata.ngo_name))
                    ngo_id = n2.id


        else:
            n=ngodata.objects.get(ngo_name=ngo)
            print(str(n.user_id) + n.ngo_name)
            ngo_id=n.user_id


        if (0 < int(quantity) <= 20):
            mode = "doorstep"
            time = request.POST['time']
        else:
            mode = request.POST['mode']
            if mode=='doorstep':
                time = 'none'
            else :
                time = request.POST['time']


        date = datetime.date.today()
        uid = request.user.id
        data = donation_data(donor_id=uid, ngo_id=ngo_id, address=address, sector=sector, category=category,
                             quantity=quantity, mode=mode, pickup_time=time, date=date)
        data.save()
        n= User.objects.get(id=ngo_id)

        message = 'NGO name:' + n.ngodata.ngo_name + '\n time:'+ time + '\n NGO address:'+ n.address +'\n Type:'+ sector +'\n Mode: '+mode
        print(message)
        send_mail(
            'Raise_Donation ',
            message,
            settings.EMAIL_HOST_USER,
            [email], fail_silently=False)
        messages.info(request, 'successfully Donated')
        return redirect('/')



    else:

         dests = ""
         if request.session.has_key('ngo_id') :
               ngo_id = int(request.session['ngo_id'])
               print(ngo_id)
               dests = ngodata.objects.filter(user_id=ngo_id)
               del request.session['ngo_id']
         else:
              dests = ngodata.objects.filter(sector__contains='Food')
         return render(request, "food.html", { 'dests': dests })


# books donation
def Books(request):
    if request.method == 'POST':
        email = request.POST['email']
        address = request.POST['address']
        sector = request.POST['sector']
        print(sector)
        category = request.POST.getlist('category')
        ngo = request.POST['ngo']
        quantity = request.POST['quantity']
        cat = ""
        for i in category:
            cat = cat + i
            cat = cat + " "

        print(cat)
        if ngo=='none':
            r1=requests.objects.filter(sector__contains='Books')

            if r1 is None :
                n1=User.objects.filter(type='ngo')
                n2=random.choices(n1)
                print(n2.id + n2.ngodata.ngo_name)
                ngo_id=n2.id
            else:

                r2=belongs_to.objects.filter(request_id__in=r1, request_to='donors').values_list('ngo_id')
                if r2  :
                    print('id')
                    print(len(r2))
                    for x in range(len(r2)):
                        print(r2[x])
                    r3= random.choices(r2)
                    print(r3[0][0])
                    ngo_id= r3[0][0]
                    print(str(ngo_id))
                else:
                    n1 = User.objects.filter(type='ngo')
                    n2 = random.choice(n1)
                    print(str(n2.id) + str(n2.ngodata.ngo_name))
                    ngo_id = n2.id


        else:
            n=ngodata.objects.get(ngo_name=ngo)
            print(str(n.user_id) + n.ngo_name)
            ngo_id=n.user_id


        if (0 < int(quantity) <= 20):
            mode = "doorstep"
            time = request.POST['time']
        else:
            mode = request.POST['mode']
            if mode=='doorstep':
                time = 'none'
            else :
                time = request.POST['time']


        date = datetime.date.today()
        uid = request.user.id

        data = donation_data(donor_id=uid, ngo_id=ngo_id, address=address, sector=sector, category=cat,
                             quantity=quantity, mode=mode, pickup_time=time, date=date)
        data.save()
        n = User.objects.get(id=ngo_id)

        message = 'NGO name:' + n.ngodata.ngo_name + '\n time:' + time + '\n NGO address:' + n.address + '\n Type:' + sector + '\n Mode: ' + mode
        print(message)
        send_mail(
            'Raise_Donation ',
            message,
            settings.EMAIL_HOST_USER,
            [email], fail_silently=False)
        messages.info(request, 'successfully Donated')
        return redirect('/')

    else:
        dests = ""
        if request.session.has_key('ngo_id'):
            ngo_id = int(request.session['ngo_id'])
            print(ngo_id)
            dests = ngodata.objects.filter(user_id=ngo_id)
            del request.session['ngo_id']
        else:
            dests = ngodata.objects.filter(sector__contains='Books')
        return render(request, "book.html", {'dests': dests})


#clothes donations
def Clothes(request):
    if request.method == 'POST':
        email = request.POST['email']
        address = request.POST['address']
        sector = request.POST['sector']
        category = request.POST['category']
        ngo = request.POST['ngo']
        quantity = request.POST['quantity']
        if ngo=='none':
            r1=requests.objects.filter(sector__contains='Clothes')

            if r1 is None :
                n1=User.objects.filter(type='ngo')
                n2=random.choices(n1)
                print(n2.id + n2.ngodata.ngo_name)
                ngo_id=n2.id
            else:

                r2=belongs_to.objects.filter(request_id__in=r1, request_to='donors').values_list('ngo_id')
                if r2  :
                    print('id')
                    print(len(r2))
                    for x in range(len(r2)):
                        print(r2[x])
                    r3= random.choices(r2)
                    print(r3[0][0])
                    ngo_id= r3[0][0]
                    print(str(ngo_id))
                else:
                    n1 = User.objects.filter(type='ngo')
                    n2 = random.choice(n1)
                    print(str(n2.id) + str(n2.ngodata.ngo_name))
                    ngo_id = n2.id


        else:
            n=ngodata.objects.get(ngo_name=ngo)
            print(str(n.user_id) + n.ngo_name)
            ngo_id=n.user_id


        if (0 < int(quantity) <= 20):
            mode = "doorstep"
            time = request.POST['time']
        else:
            mode = request.POST['mode']
            if mode=='doorstep':
                time = 'none'
            else :
                time = request.POST['time']


        date = datetime.date.today()
        uid = request.user.id
        data = donation_data(donor_id=uid, ngo_id=ngo_id, address=address, sector=sector, category=category,
                             quantity=quantity, mode=mode, pickup_time=time, date=date)
        data.save()
        n = User.objects.get(id=ngo_id)

        message = 'NGO name:' + n.ngodata.ngo_name + '\n time:' + time + '\n NGO address:' + n.address + '\n Type:' + sector + '\n Mode: ' + mode
        print(message)
        send_mail(
            'Raise_Donation ',
            message,
            settings.EMAIL_HOST_USER,
            [email], fail_silently=False)
        messages.info(request, 'successfully Donated')
        return redirect('/')

    else:
        dests = ""
        if request.session.has_key('ngo_id'):
            ngo_id = int(request.session['ngo_id'])
            print(ngo_id)
            dests = ngodata.objects.filter(user_id=ngo_id)
            del request.session['ngo_id']
        else:
            dests = ngodata.objects.filter(sector__contains='Clothes')
        return render(request, "clothes.html", {'dests': dests})



def logout(request):
    auth.logout(request)
    return redirect('/') 



