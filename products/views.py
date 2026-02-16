from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from .filters import ProductFilter


def catalog(request):
    queryset = Product.objects.filter(stock__gt=0).select_related('category').prefetch_related('images')
    product_filter = ProductFilter(request.GET, queryset=queryset)
    categories = Category.objects.filter(parent__isnull=True).prefetch_related('children')

    return render(request, 'products/catalog.html', {
        'filter': product_filter,
        'products': product_filter.qs,
        'categories': categories,
        'current_category': request.GET.get('category', ''),
        'current_sort': request.GET.get('sort', ''),
    })


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category').prefetch_related('images'),
        slug=slug
    )
    related_products = Product.objects.filter(
        category=product.category, stock__gt=0
    ).exclude(pk=product.pk).prefetch_related('images')[:4]

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = product.favorites.filter(user=request.user).exists()

    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'is_favorite': is_favorite,
    })
