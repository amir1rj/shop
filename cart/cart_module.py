from itertools import product

from products.models import Product

CART_SESSION_ID = 'cart'
class Cart:
    def __init__(self,request):
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()
        for item in cart.values():
            product =Product.objects.get(id=item["id"])
            item["product"] = product
            item["total"] = int(item["quantity"]) * int(item["price"])
            item["unique_id"] = self.unique_id_generator(product.id,item["color"],item["size"])
            yield item
    def save(self):
        self.session.modified = True
    def delete(self,id):
        del self.cart[id]
        self.save()

    def unique_id_generator(self,id,color,size):
        result=f"{id}_{color}_{size}"
        return result
    def total(self):
        cart =self.cart
        total_price = 0
        for item in cart.values():
            total_price+=int(item["quantity"]) * int(item["price"])
        return total_price
    def remove(self):
        del self.session["cart"]
    def add(self,product,quantity,size,color):
        unique_id =self.unique_id_generator(product.id,color,size)
        if unique_id not in self.cart:
            self.cart[unique_id]={"price":str(product.price),"color":color,"size":size,"id":product.id,"quantity":0}
        self.cart[unique_id]["quantity"] += int(quantity)
        self.save()


#
#
# from products.models import Product
#
# CART_SESSION_ID="cart"
# class Cart:
#     def __init__(self,request):
#         self.session = request.session
#         cart = self.session.get("cart")
#         if not cart:
#             cart = self.session["cart"] = {}
#         self.cart = cart
#     def __iter__(self):
#         cart =self.cart.copy()
#         for item in cart.values():
#             item["product"] = Product.objects.get(id=item["id"])
#             item["total"] = int(item["price"])*int(item["quantity"])
#             yield item
#
#     def unique(self,product,size,color):
#         return f"{product.id}-{size}-{color}"
#     def add(self,product,quantity,size,color):
#         un = self.unique(product,size,color)
#         if not un:
#             self.cart[un]={"quantity":0,"color":color,"size":size,"price":str(product.price),"id":product.id}
#         self.cart[un]['quantity']+=int(quantity)
#         self.save()
#     def save(self):
#         self.session.modified = True
#


