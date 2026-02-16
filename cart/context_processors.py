from django.utils.deprecation import MiddlewareMixin


def cart_context(request):
    """Add cart item count to all templates."""
    cart = request.session.get('cart', {})
    cart_count = sum(item.get('quantity', 0) for item in cart.values())
    return {'cart_count': cart_count}


class CartMiddleware(MiddlewareMixin):
    """Ensure session cart exists."""
    def process_request(self, request):
        if 'cart' not in request.session:
            request.session['cart'] = {}
