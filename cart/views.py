from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Order, OrderItem
from .telegram import send_order_notification
from decimal import Decimal


def _get_cart(request):
    """Get cart dict from session."""
    return request.session.get('cart', {})


def _save_cart(request, cart):
    """Save cart dict to session."""
    request.session['cart'] = cart
    request.session.modified = True


def add_to_cart(request, product_id):
    """Add a product to the cart (AJAX or regular)."""
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id, stock__gt=0)
        cart = _get_cart(request)
        product_key = str(product_id)
        quantity = int(request.POST.get('quantity', 1))

        if product_key in cart:
            cart[product_key]['quantity'] += quantity
        else:
            cart[product_key] = {
                'quantity': quantity,
                'price': str(product.price),
                'name': product.name,
            }

        if cart[product_key]['quantity'] > product.stock:
            cart[product_key]['quantity'] = product.stock

        _save_cart(request, cart)

        cart_count = sum(item['quantity'] for item in cart.values())

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': f'{product.name} added to cart',
                'cart_count': cart_count,
            })

        messages.success(request, f'{product.name} added to cart!')
        return redirect(request.META.get('HTTP_REFERER', 'core:home'))

    return redirect('core:home')


def cart_detail(request):
    """View shopping cart."""
    cart = _get_cart(request)
    cart_items = []
    total = Decimal('0.00')

    for product_id, item in cart.items():
        try:
            product = Product.objects.prefetch_related('images').get(pk=int(product_id))
            subtotal = Decimal(item['price']) * item['quantity']
            cart_items.append({
                'product': product,
                'quantity': item['quantity'],
                'price': Decimal(item['price']),
                'subtotal': subtotal,
            })
            total += subtotal
        except Product.DoesNotExist:
            continue

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


def update_cart(request, product_id):
    """Update quantity of a cart item."""
    if request.method == 'POST':
        cart = _get_cart(request)
        product_key = str(product_id)
        quantity = int(request.POST.get('quantity', 1))

        if product_key in cart:
            if quantity <= 0:
                del cart[product_key]
            else:
                product = get_object_or_404(Product, pk=product_id)
                if quantity > product.stock:
                    quantity = product.stock
                cart[product_key]['quantity'] = quantity

        _save_cart(request, cart)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            cart_count = sum(item['quantity'] for item in cart.values())
            return JsonResponse({'status': 'success', 'cart_count': cart_count})

    return redirect('cart:cart_detail')


def remove_from_cart(request, product_id):
    """Remove item from cart."""
    cart = _get_cart(request)
    product_key = str(product_id)
    if product_key in cart:
        del cart[product_key]
        _save_cart(request, cart)
        messages.info(request, 'Item removed from cart.')

    return redirect('cart:cart_detail')


def checkout(request):
    """Checkout page and order placement."""
    cart = _get_cart(request)
    if not cart:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:cart_detail')

    cart_items = []
    total = Decimal('0.00')

    for product_id, item in cart.items():
        try:
            product = Product.objects.get(pk=int(product_id))
            subtotal = Decimal(item['price']) * item['quantity']
            cart_items.append({
                'product': product,
                'quantity': item['quantity'],
                'price': Decimal(item['price']),
                'subtotal': subtotal,
            })
            total += subtotal
        except Product.DoesNotExist:
            continue

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        note = request.POST.get('note', '').strip()

        if not all([full_name, phone, address, city]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'cart/checkout.html', {
                'cart_items': cart_items,
                'total': total,
            })

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            phone=phone,
            address=address,
            city=city,
            note=note,
            total_price=total,
        )

        for cart_item in cart_items:
            product = cart_item['product']
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                quantity=cart_item['quantity'],
                price=cart_item['price'],
            )
            product.stock -= cart_item['quantity']
            product.save()

        # Send Telegram notification
        send_order_notification(order)

        # Clear cart
        request.session['cart'] = {}
        request.session.modified = True

        return redirect('cart:order_success', order_id=order.pk)

    # Pre-fill from profile if user is authenticated
    initial = {}
    if request.user.is_authenticated:
        user = request.user
        initial = {
            'full_name': user.get_full_name() or user.username,
            'phone': getattr(user, 'profile', None) and user.profile.phone or '',
            'address': getattr(user, 'profile', None) and user.profile.address or '',
            'city': getattr(user, 'profile', None) and user.profile.city or '',
        }

    return render(request, 'cart/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'initial': initial,
    })


def order_success(request, order_id):
    """Order confirmation page."""
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'cart/order_success.html', {'order': order})


@login_required
def order_history(request):
    """User's order history."""
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'cart/order_history.html', {'orders': orders})
