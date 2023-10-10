from django.contrib import admin
from .models import *


class ImageInline(admin.TabularInline):
    model = Image
class InformationInline(admin.StackedInline):
    model = Information


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "discount",)
    list_editable = ("price", "discount")
    list_filter = ("price", "discount")
    inlines = (ImageInline,InformationInline)
    list_display_links = ("title",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "parent")
    prepopulated_fields = {"slug": ("title",)}





admin.site.register(Size)
admin.site.register(Color)
admin.site.register(CouponCode)

