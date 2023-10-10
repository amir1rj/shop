from django.shortcuts import render, redirect,get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from cart.cart_module import Cart
from cart.models import Order, OrderItem
from products.models import Product, Size, Color, CouponCode


# Create your views here.
class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'cart/cart_detail.html',{"cart": cart})

class CartAddView(View):
    def post(self, request,pk):
        product =get_object_or_404(Product,id=pk)
        color ,size,quantity =request.POST.get('color'),request.POST.get('size'),request.POST.get('quantity')
        cart = Cart(request)
        cart.add(product,quantity,size,color)   #   add to cart list
        return redirect('cart:cart_detail')
class CartDeleteView(View):
    def get(self, request,id):
        cart = Cart(request)
        cart.delete(id)
        return redirect('cart:cart_detail')

class AddOrderView(LoginRequiredMixin,View):
    def get(self, request):
        cart = Cart(request)
        order =Order.objects.create(user=request.user,total=cart.total())
        for item in cart:
            quantity,price =item["quantity"],item["price"]
            size = Size.objects.get(title=item["size"])
            color = Color.objects.get(title=item["color"])
            product = Product.objects.get(title=item["product"])
            print(item["color"])
            OrderItem.objects.create(order=order,product=product,size=size,color=color,quantity=quantity,price=price)

        cart.remove()
        return redirect('cart:order_detail',order.id)

class OrderDetailView(LoginRequiredMixin,View):
    def get(self, request,pk):
        order = get_object_or_404(Order,id=pk)
        return render(request,'cart/oerder_detail.html',{'order':order})

class ApplyCouponView(LoginRequiredMixin,View):
    def post(self,request,pk):
        order = get_object_or_404(Order,id=pk)
        code = request.POST.get('coupon')
        coupon = get_object_or_404(CouponCode,code=code)
        print(code)
        if coupon.quantity >=1:
            if coupon.type == "percent":
                order.total -= order.total*(coupon.amount/100)
                coupon.quantity -=1
            elif coupon.type == "value":
                order.total -= coupon.amount
                coupon.quantity -= 1
        coupon.save()
        order.save()
        return redirect('cart:order_detail',order.id)

