from django.db import models

from account.models import User
from products.models import Product, Color, Size


# Create your models here.
class Order(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE,related_name="orders")
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    address =models.TextField(blank=True,null=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name="items")

    size = models.ForeignKey(Size, on_delete=models.CASCADE,)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name="colors")
    quantity = models.IntegerField()
    price = models.PositiveIntegerField()
    def __str__(self):
        return self.product.title
