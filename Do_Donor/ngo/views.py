from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.models import auth,User
from account.models import User
from .models import ngodata
from donation.models import donation_data
from django.contrib import  messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Sum
import random
import math
from django.views.decorators.cache import cache_control
import datetime
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from notification.views import noti,mark,remove,removeAll,markAll,sendNotify
from request.views import ask_ngo,request_donor
from notification.views import interest
from request.views import your_request,delete



def ngo(request):
     request.session.flush()
     return render(request, "ngo.html")


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_protect
def notp(request):
     if request.method == 'POST' :
          r_no = request.POST['r_no']
          username = request.POST['username']
          ngo_name =  request.POST['ngo_name']
          password= request.POST['password']
          c_password = request.POST['cpassword']
          name = request.POST['name']
          img = request.FILES['image']
          fs = FileSystemStorage()
          fs.save(img.name, img)
          email =  request.POST['email']
          address =  request.POST['address']
          mobile =  request.POST['mobile']
          zip = request.POST['zip']
          sector = request.POST.getlist('sector')
          desc =  request.POST['desc']

          cat = ""
          for i in sector:
                cat = cat + i
                cat = cat + " "
          if password==c_password:

              if User.objects.filter(email=email).exists():

                  messages.info(request, 'email already exist')
                  return redirect('ngo')
              elif User.objects.filter(username=username).exists():

                  messages.info(request, 'username already exist')
                  return redirect('ngo')
              elif ngodata.objects.filter(r_no=r_no).exists():

                  messages.info(request, 'registration no. already exist')
                  return redirect('ngo')
              elif ngodata.objects.filter(ngo_name=ngo_name).exists():

                  messages.info(request, 'ngo_name  already exist')
                  return redirect('ngo')

              else:
                  request.session['r_no'] = r_no
                  request.session['username'] = username
                  request.session['ngo_name'] = ngo_name
                  request.session['password'] = password
                  request.session['email'] = email
                  request.session['address'] = address
                  request.session['mobile'] = mobile
                  request.session['name'] = name
                  request.session['img'] = img.name
                  request.session['zip'] = zip
                  request.session['cat'] = cat
                  request.session['desc'] = desc
                  request.session['notp'] = generate_otp()
                  context = RequestContext(request)
                  context['notp'] = request.session['notp']
                  message = 'your six digit otp is ' + str(request.session['notp'])
                  send_mail(
                       'Do Donor.com ',
                       message,
                       settings.EMAIL_HOST_USER,
                       [email], fail_silently=False)
                  return render(request, "notp.html")

          else:
              print('password did not matched')
              messages.info(request, 'password did not match')
              return redirect('ngo')


     else:
          if request.session.has_key('value'):
               return render(request, "reset_password.html")

          elif request.session.has_key('e_email'):
              n = User.objects.get(id=request.session['id'])
              n.email = request.session['e_email']
              n.address = request.session['e_address']
              n.mobile = request.session['e_mobile']
              n.ngodata.sector = request.session['e_sector']
              n.save()
              n.ngodata.save()


              print('email new changed')
              return redirect('ngopannel')

          else:

              user = User(name=request.session['name'], email=request.session['email'], username=request.session['username'],
                          mobile=request.session['mobile'], address=request.session['address'], type='ngo')
              user.set_password(request.session['password'])
              user.save();
              user = User.objects.get(username=request.session['username'])
              print(user.username)
              print(request.session['r_no'])
              n = ngodata(user_id=user.id, r_no=request.session['r_no'], ngo_name=request.session['ngo_name'], zip=request.session['zip'], img=request.session['img'], sector=request.session['cat'], desc=request.session['desc'])

              n.save();
              print('ngo registered')
              email = request.session['email']
              message = 'you have been successfully registered as ngo'
              send_mail(
                    'Do Donor.com ',
                    message,
                    settings.EMAIL_HOST_USER,
                    [email], fail_silently=False)

              return redirect('nlogin')


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def nlogin(request):
    if request.method == 'POST':

        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)


        if user is not None:
            u = User.objects.get(email=email)
            if u.type == 'ngo' :

               auth.login(request, user)
               messages.success(request, 'logged in successfully')
               return redirect('ngopannel')

            else:
                messages.success(request, 'invalid credentials')
                return redirect('nlogin')
        else:
            messages.success(request, 'invalid credentials')
            return redirect('nlogin')

    else:

        return render(request, "nlogin.html")


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
# user logout views here.
def nlogout(request):
    auth.logout(request)
    return redirect('/')



def generate_otp():
    string = '0123456789'
    otp = ""
    length= len(string)
    for i in range(6):
        otp += string[math.floor(random.random()* length)]
    return otp


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def resendotp(request):
    message = 'your six digit otp is ' + str(request.session['notp'])
    email = request.session['email']
    send_mail(
        'Do Donor.com ',
        message,
        settings.EMAIL_HOST_USER,
        [email], fail_silently=False)
    return HttpResponse("again otp is sent to your mail")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def forgot_password(request):
    value = request.POST.get('fp')
    request.session['value']=value
    print(value)
    return render(request, "email_otp.html" )

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def email_otp(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            request.session['email'] = email
            request.session['otp'] = generate_otp()
            context = RequestContext(request)
            context['otp'] = request.session['otp']
            message = 'your six digit otp is ' + str(request.session['otp'])
            send_mail(
                'Do Donor.com ',
                message,
                settings.EMAIL_HOST_USER,
                [email], fail_silently=False)
            return render(request, "notp.html")
        else:
            print('email not registered')
            messages.info(request, 'email not registered')
            return redirect('email_otp')

    return render(request, "email_otp.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reset_password(request):
    if request.method == 'POST':
        email=request.session['email']
        password = request.POST['password']
        c_password = request.POST['c_password']
        if password == c_password:
            u = User.objects.get(email=email)
            u.set_password(password)
            u.save()
            request.session.flush()
            return redirect('nlogin')
        else:
            print('password did not matched')
            messages.info(request, 'password did not match')
            return render(request, "reset_password.html")

    return render(request, "reset_password.html")









@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ngopannel(request) :
    if request.user.is_authenticated:
        u1 = request.user.username
        n = User.objects.get(username=u1)
        print(n.name)
        ngo_collection = donation_data.objects.filter(ngo_id=request.user.id).order_by('-date')
        sector= ngodata.objects.filter(user_id=request.user.id).values_list('sector')
        print(sector[0][0])
        list1= sector[0][0].split(" ")
        print(list1)
        list2= []
        j= 0
        for i in list1 :
          sec = donation_data.objects.filter(ngo_id=request.user.id, sector=i).aggregate(Sum('quantity'))
          sector= sec["quantity__sum"]
          list2.append(list1[j] + " recieved :" + str(sector))
          j=j+1
        amount = donation_data.objects.filter(ngo_id=request.user.id).aggregate(Sum('amount'))
        return render(request, 'ngopannel.html', { 'ngo_collection': ngo_collection, 'list2': list2,'amount': amount["amount__sum"]})


def ngo_request(request):
    return render(request, "ngo_request.html")










def ngo_edit(request):
    if request.user.is_authenticated:
        u1 = request.user.id
        n = User.objects.get(id=u1)

    return render(request, "ngo_edit.html", {'ngo_name': n.ngodata.ngo_name, 'email': n.email, 'address': n.address, 'mobile': n.mobile})



def basic_edit(request):
    if request.method == 'POST':
        email = request.POST['email']
        address = request.POST['address']
        mobile = request.POST['mobile']
        sector = request.POST.getlist('sector')

        cat = ""
        for i in sector:
            cat = cat + i
            cat = cat + " "
        print(cat)
        n = User.objects.get(id=request.user.id)
        if email != n.email :
            request.session['e_email'] = email
            request.session['e_address'] = address
            request.session['e_address'] = mobile
            request.session['e_sector'] = cat
            request.session['otp'] = generate_otp()
            context = RequestContext(request)
            context['otp'] = request.session['otp']
            message = 'your six digit otp is ' + str(request.session['otp'])
            send_mail(
                'Do Donor.com ',
                message,
                settings.EMAIL_HOST_USER,
                [email], fail_silently=False)
            return render(request, "notp.html")

        n.address= address
        n.mobile= mobile
        n.ngodata.sector = cat
        print('email old changed')
        n.save()
        n.ngodata.save()

        return redirect('ngopannel')

# user change password views here.
def change_password(request):
     if request.method == 'POST':
        old_p= request.POST['old']
        new_p= request.POST['new']
        confirm_p= request.POST['confirm']
        n = User.objects.get(id=request.user.id)
        if old_p == n.password  :
            if old_p == new_p :
                print('password is same')
                messages.info(request, 'password is same!')
                return redirect('ngo_edit')

            elif new_p == confirm_p:

                n.set_password(new_p)
                n.save()
                print('password is changed successfully')
                request.session.flush()
                return redirect('nlogin')
            else:
                print('Something is wrong')
                messages.info(request, 'something is wrong!')
                return redirect('ngo_edit')
        else:
         print('password is not matching')
         messages.info(request, 'password is not matching!')
         return redirect('ngo_edit')





