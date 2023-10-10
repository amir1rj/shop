from django.contrib import messages
from django.contrib.auth import login,authenticate,logout,update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect,reverse
from django.utils.crypto import get_random_string
from django.views import View
from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from Lshoper.celery import app
from .forms import LoginForm, RegisterForm, CheckOptForm, AddAdressForm
import ghasedakpack
import random
from .models import Otp, User, Address


import time

from .tasks import delete_expire_code




SMS = ghasedakpack.Ghasedak("4b49f78a727dfaabb5e3ab94adca3f1629ff577b7d38ff29f89ac39a26bd5467")

class UserLogin(View):
    def get(self,request):
        form = LoginForm()
        return render(request,"account/login.html",{"form":form})
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd =form.cleaned_data
            user = authenticate(username=cd.get('username'), password=cd.get('password'))
            if user is not None:
                login(request, user)
                next = request.GET.get("next")
                if next:
                    return redirect(next)
                return redirect('/')
            else:
                form.add_error("username", "Invalid username or password")
        else:
            form.add_error("username", "Invalid data")
        return render(request,"account/login.html",{"form":form})
class UserRegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "account/register.html", {"form": form})
    def post(self,request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            token = get_random_string(100)
            cd =form.cleaned_data
            email,username,phone_number,password= cd["email"],cd["username"],cd["phone_number"],cd["password"]
            randcode =random.randint(1000,9999)
            print(randcode)
            # SMS.verification({'receptor': cd["phone_number"], 'type': '1', 'template': 'randomcode', 'param1':randcode })
            obj= Otp.objects.create(phone_number=phone_number,email=email,username=username,randcode=randcode,token=token,password=password)
            delete_expire_code.delay(username)

            return redirect(reverse('account:checkOpt')+f"?token={token}")
        else:
            form.add_error("phone_number", "Invalid data")

        return render(request,"account/register.html",{"form":form})

class CheckOptView(View):
    def get(self, request):
        form=CheckOptForm()
        return render(request, "account/check_OTP.html", {"form":form})
    def post(self, request):
        token=request.GET.get('token')
        form=CheckOptForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Otp.objects.filter(randcode=cd.get('expire_code'),token=token).exists():
                otp= Otp.objects.get(token=token)
                user=User.objects.create(phone_number=otp.phone_number,email=otp.email,username=otp.username)
                user.set_password(otp.password)
                user.save()
                login( request,user,backend="django.contrib.auth.backends.ModelBackend")
                next = request.GET.get('next')
                if next:
                    return redirect(next)
                otp.delete()
                return redirect('/')
        else:
            form.add_error("expire_code", "Invalid code")
        if form.is_valid():
            form.add_error("expire_code", "Invalid code")

        return render(request, "account/check_OTP.html", {"form": form})

def user_loguot(request):

    logout(request)
    return redirect("/")

def change_password(request):
    if request.method == "POST" :
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            # messages.success((request,"your password was successfully changed"))
            return redirect("/")
        else: messages.error(request,"please correct the error below")
    else:
        form = PasswordChangeForm(request.user)
    return render(request,'account/change_password.html',{"form":form})

class AddAdressView(LoginRequiredMixin,View):
    def get(self, request):
        form = AddAdressForm()


        return render(request, "account/add_address.html", {"form": form})
    def post(self, request):
        form = AddAdressForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            email,address,phone,postal_code,name,city=cd["email"],cd["address"],cd["phone"],cd["postal_code"],cd["full_name"],cd["city"]
            Address.objects.create(email=email,address=address,phone=phone,postal_code=postal_code,city=city,full_name=name,user=request.user)
            next = request.GET.get("next")
            if next:
                return redirect(next)
            return redirect("/")





