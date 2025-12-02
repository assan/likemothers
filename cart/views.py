from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from django.contrib import messages
from orders.views import order_create  # Для перехода к заказу

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    qty = int(request.POST.get('quantity', 1))

    # Обработка кнопок + и −
    if 'add' in request.POST:
        qty = cart.cart.get(str(product.id), {}).get('qty', 0) + 1
    elif 'subtract' in request.POST:
        qty = cart.cart.get(str(product.id), {}).get('qty', 0) - 1
        if qty <= 0:
            cart.remove(product)
            messages.success(request, f"{product.name} удалён из корзины")
            return redirect('cart:cart_detail')

    if qty > product.stock:
        messages.error(request, f"В наличии только {product.stock} порций!")
        return redirect('cart:cart_detail')

    cart.add(product=product, qty=qty, update_qty=True)
    messages.success(request, f"Количество обновлено")
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})