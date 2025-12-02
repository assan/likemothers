from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from cart.cart import Cart
from .models import Order, OrderItem
from .utils import calculate_delivery


@require_POST
def order_create(request):
    cart = Cart(request)
    if not cart:
        return redirect('shop:product_list')

    order = Order.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        phone=request.POST['phone'],
        address=request.POST['address'],
        postal_code=request.POST.get('postal_code', ''),
        city='Алматы',
        delivery_time=request.POST.get('delivery_time', ''),
        comment=request.POST.get('comment', ''),
    )

    delivery_price = calculate_delivery(request.POST['address'], cart.get_total_price())
    order.delivery_price = delivery_price
    order.save()

    # Создаём элементы заказа и уменьшаем остаток
    for item in cart:
        product = item['product']
        qty = item['qty']

        if product.stock < qty:
            messages.error(request, f"Товара «{product.name}» недостаточно на складе!")
            order.delete()
            return redirect('cart:cart_detail')

        OrderItem.objects.create(order=order, product=product, price=item['price'], quantity=qty)

        # ←←← УМЕНЬШАЕМ ОСТАТОК
        product.stock -= qty
        product.save()

    cart.clear()
    messages.success(request, "Заказ успешно создан! Переходим к оплате…")

    # Переходим к оплате
    from payments.views import payment_process
    return payment_process(request, order.id)