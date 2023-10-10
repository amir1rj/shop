from django.contrib import admin

from cart.models import Order, OrderItem


# Register your models here.
class ItemModelAdmin(admin.TabularInline):
    model = OrderItem

@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    Model = Order
    list_filter = ("is_paid",)
    list_display = ("user","is_paid","user")
    list_editable = ("is_paid",)
    inlines = (ItemModelAdmin,)

