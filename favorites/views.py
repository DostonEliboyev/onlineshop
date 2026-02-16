from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Favorite
from products.models import Product


@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product__category').prefetch_related('product__images')
    return render(request, 'favorites/favorites.html', {
        'favorites': favorites,
    })


@login_required
def toggle_favorite(request, product_id):
    if request.method == 'POST':
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)

        favorite, created = Favorite.objects.get_or_create(
            user=request.user, product=product
        )

        if not created:
            favorite.delete()
            return JsonResponse({'status': 'removed', 'message': 'Removed from favorites'})

        return JsonResponse({'status': 'added', 'message': 'Added to favorites'})

    return JsonResponse({'error': 'Invalid request'}, status=400)
