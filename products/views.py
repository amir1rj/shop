from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, TemplateView, ListView

from products.models import Product, Category, Color, Size


# Create your views here.
class ProductDetailView(DetailView):
    model = Product
class CategoryView(TemplateView):
    template_name = "inclodes/category.html"
    def get_context_data(self):
        context = super(CategoryView, self).get_context_data()
        context["categories"] = Category.objects.all()
        return context

class ProductsListView(ListView):
    template_name = "products/product_list.html"
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        request = self.request
        colors , sizes = request.GET.getlist('color'), request.GET.getlist('size')
        max,min = request.GET.get('max_price'),request.GET.get('min_price')
        queryset = Product.objects.all()
        page_number = self.request.GET.get('page')
        paginator = Paginator(queryset, 1)
        object_list = paginator.get_page(page_number)
        if colors:
            queryset = queryset.filter(color__title__in=colors).distinct()
        if sizes:
            queryset = queryset.filter(size__title__in=sizes).distinct()
        if max or min:
            if not min:
                min = 0
            if not max:
                max = 9999999999999999
            queryset = queryset.filter(price__gte=min)
            queryset = queryset.filter(price__lte=max)
        data["object_list"] = object_list
        data['colors'] = Color.objects.all()
        data['sizes'] = Size.objects.all()
        return data

class CategoryListView(View):
    def get(self, queryset,slug):
        queryset = Product.objects.filter(category__slug=slug)
        page_number = self.request.GET.get('page')
        paginator = Paginator(queryset,1)
        object_list = paginator.get_page(page_number)


        data = {"object_list": object_list}
        data['colors'] = Color.objects.all()
        data['sizes'] = Size.objects.all()

        return render(self.request,"products/product_list.html",data)













