from django.shortcuts import render, redirect,HttpResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import auth,User
from .models import User
from ngo.models import ngodata
from donation.models import donation_data
from django.core.mail import send_mail
import random
import math
from django.views.decorators.cache import cache_control
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.db.models import Sum

from request.views import user_request
from notification.views import noti,mark,remove,removeAll,markAll,sendNotify
from donation.views import Food,Clothes,Books,charity,donation
from request.views import your_request,delete
# user registrtion views here.
def register(request):
    return render(request, "register.html")


# user otp views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_protect
def otp(request):
    # user registration post method before otp verification views here.
   if request.method == 'POST':
          first_name = request.POST['first_name']
          last_name = request.POST['last_name']
          email = request.POST['email']
          address = request.POST['address']
          mobile = request.POST['mobile']
          username = request.POST['username']
          password = request.POST['password']
          c_password = request.POST['confirm password']

          if password==c_password:
              if User.objects.filter(username=username).exists():
                  print('username taken')
                  messages.info(request, 'username already taken')
                  return redirect('register')
              elif User.objects.filter(email=email).exists():
                  print('email taken')
                  messages.info(request, 'email already exist')
                  return redirect('register')
              else:
                  request.session['first_name'] = first_name
                  request.session['last_name'] = last_name
                  request.session['email'] = email
                  request.session['address'] = address
                  request.session['mobile'] = mobile
                  request.session['username'] = username
                  request.session['password'] = password
                  request.session['otp']= generateotp()
                  context = RequestContext(request)
                  context['otp'] = request.session['otp']
                  message = 'your six digit otp is ' + str(request.session['otp'])
                  send_mail(
                      'Do Donor.com ',
                      message,
                      settings.EMAIL_HOST_USER,
                      [email], fail_silently=False)
                  return render(request, "otp.html")
          else:
              print('password did not matched')
              messages.info(request, 'password did not match')
              return redirect('register')

   else:
       # user reset password after otp verification views here.
       if request.session.has_key('value'):
               return render(request, "reset_password.html")

       # user edit detail after new email otp verification here.
       elif request.session.has_key('e_email'):
               user = User.objects.get(id=request.user.id)
               user.email=request.session['e_email']
               user.address= request.session['e_address']
               user.mobile= request.session['e_mobile']
               user.save()
               print('email new changed')
               return redirect('profile')

       # user registration after otp verifications views here.
       else:
               name = request.session['first_name'] + " " + request.session['last_name']
               user = User(name=name, email=request.session['email'], username=request.session['username'], mobile=request.session['mobile'], address=request.session['address'], type='donor')
               user.set_password(request.session['password'])
               user.save();
               print('user created')
               email=request.session['email']
               message = 'you have been successfully registered'
               send_mail(
                   'Do Donor.com ',
                   message,
                   settings.EMAIL_HOST_USER,
                   [email], fail_silently=False)
               request.session.flush()
               return redirect('login')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):

   if request.method == 'POST':

          email = request.POST['email']
          password = request.POST['passwords']
          user = auth.authenticate( email=email, password=password)

          if user is not None:
              u = User.objects.get(email=email)
              if u.type == 'donor':
                  auth.login(request, user)
                  messages.success(request, 'logged in successfully')
                  return redirect('/')
              else:
                  messages.success(request, 'invalid credentials')
                  return redirect('login')
          else:
              messages.success(request, 'invalid credentials')
              return redirect('login')

   else:

       return render(request, "login.html")


# user logout views here.
def logout(request):
    auth.logout(request)
    return redirect('/')


# user otp generation function here.
def generateotp():
    string = '0123456789'
    otp = ""
    length= len(string)
    for i in range(6):
        otp += string[math.floor(random.random()* length)]
    return otp


# user resend otp views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def resend_otp(request):
    message = 'your six digit otp is ' + str(request.session['otp'])
    email = request.session['email']
    send_mail(
        'Do Donor.com ',
        message,
        settings.EMAIL_HOST_USER,
        [email], fail_silently=False)
    return HttpResponse("again otp is sent to your mail")


# user forget_password views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def forgot_password(request):
    value = request.POST.get('fp')
    request.session['value']=value
    print(value)
    return render(request, "email_otp.html" )



# user email verification for forget_password views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def email_otp(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            request.session['email'] = email
            request.session['otp'] = generateotp()
            context = RequestContext(request)
            context['otp'] = request.session['otp']
            message = 'your six digit otp is' + str(request.session['otp'])
            send_mail(
                'Do Donor.com ',
                message,
                settings.EMAIL_HOST_USER,
                [email], fail_silently=False)
            return render(request, "otp.html")
        else:
            print('email not registered')
            messages.success(request, 'email not registered')
            return redirect('email_otp')

    return render(request, "email_otp.html")

# user  reset password for forget_password views here.
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
            return redirect('login')
        else:
            print('password did not matched')
            messages.info(request, 'password did not match')
            return render(request, "reset_password.html")

    return render(request, "reset_password.html")



#---------------user profile pannel view is here -----------------------

def profile(request):


            donation = donation_data.objects.filter(donor_id=request.user.id).order_by('-date')
            food = donation_data.objects.filter(donor_id=request.user.id, sector='Food').aggregate(Sum('quantity'))
            clothes = donation_data.objects.filter(donor_id=request.user.id, sector='Clothes').aggregate(Sum('quantity'))
            books = donation_data.objects.filter(donor_id=request.user.id, sector='Books').aggregate(Sum('quantity'))
            amnt = donation_data.objects.filter(donor_id=request.user.id).aggregate(Sum('amount'))
            return render(request, "profile.html", { 'donation': donation,'food': food["quantity__sum"],'clothes': clothes["quantity__sum"],'books': books["quantity__sum"],'amount': amnt["amount__sum"]})

# user edit views here.
def user_edit(request):
    if request.user.is_authenticated:
        u1 = request.user.id
        user = User.objects.get(id=u1)

    return render(request, "edit.html", {'username': user.username, 'email': user.email, 'address': user.address,
                                         'mobile': user.mobile})

# user basic details edit views here.
def basic_edit(request):
    if request.method == 'POST':
        email = request.POST['email']
        address = request.POST['address']
        mobile = request.POST['mobile']
        user = User.objects.get(id=request.user.id)
        if email != user.email :
            request.session['e_email'] = email
            request.session['e_address'] = address
            request.session['e_address'] = mobile
            request.session['otp'] = generateotp()
            context = RequestContext(request)
            context['otp'] = request.session['otp']
            message = 'your six digit otp is ' + str(request.session['otp'])
            send_mail(
                'Do Donor.com ',
                message,
                settings.EMAIL_HOST_USER,
                [email], fail_silently=False)
            return render(request, "otp.html")

        user.address= address
        user.mobile= mobile
        print('email old changed')
        user.save()

        return redirect('profile')

# user change password views here.
def change_password(request):
     if request.method == 'POST':
        old_p= request.POST['old']
        new_p= request.POST['new']
        confirm_p= request.POST['confirm']
        if  request.user.check_password(old_p) :
            if old_p == new_p :
                print('old and new password are same')
                messages.info(request, 'password is same!')
                return redirect('user_edit')

            elif new_p == confirm_p:
                user = User.objects.get(id=request.user.id)
                user.set_password(new_p)
                user.save()
                print('password is changed successfully')
                return redirect('login')
            else:
                print('Something is wrong')
                messages.info(request, 'something is wrong!')
                return redirect('user_edit')
        else:
         print('password is not matching')
         messages.info(request, 'password is not matching!')
         return redirect('user_edit')


def reward(request):

    data= donation_data.objects.filter(donor_id=request.user.id).aggregate(Sum('quantity'),Sum('amount'))
    print(data)
    if (data["quantity__sum"] > 200 and data["quantity__sum"] < 700) :
        data = 'silver'
        print('silver')
    elif (data["quantity__sum"] <= 200 and data["quantity__sum"] > 0) :
        data = 'bronze'
        print('bronze')
    else:
        data = 'gold'
        print('gold')


    return render(request, "certificate.html", {'data': data})