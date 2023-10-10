from django.urls import path
from .views import *
app_name="product"
urlpatterns=[
    path("detail/<int:pk>",ProductDetailView.as_view(),name="detail"),
    path('category',CategoryView.as_view(),name="category"),
    path('list',ProductsListView.as_view(),name="list"),
    path('category/<str:slug>',CategoryListView.as_view(),name="category_list"),

]