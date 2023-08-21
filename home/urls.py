from django.urls import path
from .views import *
app_name="home"
urlpatterns =[
    path("",Home.as_view(),name="main")
]