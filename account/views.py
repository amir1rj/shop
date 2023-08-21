from django.contrib.auth import login,authenticate,logout
from django.shortcuts import render, redirect,reverse
from django.utils.crypto import get_random_string
from django.views import View
from .forms import LoginForm,RegisterForm,CheckOptForm
import ghasedakpack
import random

from .models import Otp, User

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
                return redirect('/')
            else:
                form.add_error("username ", "Invalid username or password")
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
            randcode =random.randint(1000,9999)
            # SMS.verification({'receptor': cd["phone_number"], 'type': '1', 'template': 'randomcode', 'param1':randcode })
            Otp.objects.create(phone_number=cd["phone_number"],randcode=randcode,token=token)
            print(randcode)
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
                user,is_created=User.objects.get_or_create(phone_number=otp.phone_number)
                login( request,user,backend="django.contrib.auth.backends.ModelBackend")
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





# def userLogin(request):
#     return render(request, 'account/login.html',{})
