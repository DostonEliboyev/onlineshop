from django.shortcuts import render
from .models import Banner
from products.models import Product, Category


def home(request):
    banners = Banner.objects.filter(is_active=True)
    categories = Category.objects.filter(parent__isnull=True)
    featured_products = Product.objects.filter(is_featured=True, stock__gt=0)[:8]
    new_arrivals = Product.objects.filter(stock__gt=0).order_by('-created_at')[:8]
    return render(request, 'core/home.html', {
        'banners': banners,
        'categories': categories,
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
    })


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    return render(request, 'core/contact.html')
