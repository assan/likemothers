import requests
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order


@csrf_exempt
def payment_process(request, order_id):
    order = Order.objects.get(id=order_id)
    total = str(order.get_total_price())

    if request.method == 'POST':
        # Создание токена оплаты
        data = {
            'PublicId': settings.CLOUDPAYMENTS_PUBLIC_ID,
            'Amount': total,
            'Currency': 'KZT',
            'InvoiceId': str(order.id),
            'AccountId': order.email,
            'Description': f'Заказ #{order.id} — Полуфабрикаты Алматы',
            'JsonData': json.dumps({
                'order_id': order.id,
                'address': order.address,
                'delivery_price': str(order.delivery_price),
            }),
            'CustomerReceipt': json.dumps({
                'Email': order.email,
                'Phone': order.phone,
                'Items': [
                    {'Name': item.product.name, 'Price': str(item.price), 'Quantity': item.quantity, 'VatRate': 12}
                    for item in order.items.all()
                ]
            }),
        }

        response = requests.post(
            'https://api.cloudpayments.ru/payments/tokens/create',
            data=data,
            auth=(settings.CLOUDPAYMENTS_PUBLIC_ID, settings.CLOUDPAYMENTS_API_SECRET),
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )

        if response.status_code == 200:
            token = response.json()['Model']['Token']
            # Перенаправление на форму оплаты
            return redirect(
                f'https://widget.cloudpayments.ru/?publicId={settings.CLOUDPAYMENTS_PUBLIC_ID}&amount={total}&currency=KZT&invoiceId={order.id}&description=Заказ&token={token}')

    return JsonResponse({'error': 'Ошибка создания платежа'})


@csrf_exempt
def payment_webhook(request):
    if request.method == 'POST':
        event = request.POST.get('Event')
        if event == 'ChargeSuccess':
            transaction_id = request.POST.get('TransactionId')
            # Обнови статус заказа
            order_id = request.POST.get('InvoiceId')
            order = Order.objects.get(id=order_id)
            order.paid = True
            order.save()
            # Отправь уведомление (email/SMS)
            return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid webhook'})