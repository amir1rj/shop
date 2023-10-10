from django.db import models

from account.models import User
class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    parent = models.ForeignKey("self",on_delete=models.CASCADE,related_name="subsets",null=True,blank=True)
    def __str__(self):
        return self.title

class Color(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name="رنگ"
        verbose_name_plural="رنگ ها"


class Size(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name="سایز"
        verbose_name_plural="سایزها"



class Product(models.Model):
    title = models.CharField(max_length=30)
    category = models.ManyToManyField(Category,related_name="products",blank=True)
    description = models.TextField()
    price = models.IntegerField()
    discount = models.SmallIntegerField(blank=True, null=True)
    color=models.ManyToManyField(Color,blank=True, related_name="products")
    size=models.ManyToManyField(Size, blank=True, related_name="products")
    created_at =models.DateTimeField(auto_now_add=True, null=True,blank=True)
    class Meta:
        verbose_name="محصول"
        verbose_name_plural="محصولات"
        ordering = ("-created_at",)
    def __str__(self):
        return self.title
class Image(models.Model):
        product = models.ForeignKey('Product',on_delete=models.CASCADE,related_name="images",null=True)
        title = models.CharField(max_length=30)
        image = models.ImageField(upload_to="products")
        class Meta:
            verbose_name = "عکس"
            verbose_name_plural = "عکس ها"
        def __str__(self):
            return self.title
class Information(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="information")
    text = models.TextField(blank=True,null=True)
    def __str__(self):
        return self.text[:30]


class CouponCode(models.Model):
    code = models.CharField(max_length=10)
    expire = models.DateField(null=True, blank=True)
    quantity = models.IntegerField(default=1)
    amount = models.PositiveIntegerField(default=0)
    description = models.CharField(max_length=70)
    type = models.CharField(max_length=7, choices=[('percent', 'percent'), ('value', 'value')], null=False)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "کد تخفیف"
        verbose_name_plural = "کد تخفیف ها"
