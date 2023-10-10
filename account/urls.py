from django.urls import path
from .views import *
app_name="account"
urlpatterns=[
    path("login",UserLogin.as_view(),name="login"),
    path("register",UserRegisterView.as_view(),name='register'),
    path("checkOpt",CheckOptView.as_view(),name='checkOpt'),
    path("logout",user_loguot,name='logout'),
    path("add_adress",AddAdressView.as_view(),name='add_address'),


]