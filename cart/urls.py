from django.urls import path
from .views import *
app_name ="cart"
urlpatterns =[
    path("detail",CartDetailView.as_view(), name="cart_detail"),
    path("add/<int:pk>",CartAddView.as_view(), name="cart_add"),
    path("delete/<str:id>",CartDeleteView.as_view(), name="cart_delete"),
    path("order/<int:pk>",OrderDetailView.as_view(), name="order_detail"),
    path("order/add",AddOrderView.as_view(), name="order_add"),
    path("applycoupon/<int:pk>",ApplyCouponView.as_view(), name="apply_coupon"),
]