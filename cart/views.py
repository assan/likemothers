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

    if qty > product.stock:
        messages.error(request, f"В наличии только {product.stock} порций этого товара!")
        return redirect('shop:product_list')   # ← безопасный редирект

    cart.add(product=product, qty=qty)
    messages.success(request, f"Добавлено {qty} × {product.name}")
    return redirect('cart:cart_detail')        # ← теперь точно работает

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})