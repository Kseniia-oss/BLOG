from django.shortcuts import render
from .models import Product  

def post_list(request):
    return render(request, 'main/post-list.html')


def product_list(request):
    products = Product.objects.all()  
    return render(request, 'main/product_list.html', {'products': products})