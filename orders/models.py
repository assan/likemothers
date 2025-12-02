# orders/models.py
from django.db import models
from shop.models import Product

class Order(models.Model):
    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50)
    email = models.EmailField('E-mail')
    phone = models.CharField('Телефон', max_length=20)
    address = models.CharField('Адрес доставки', max_length=250)
    postal_code = models.CharField('Индекс', max_length=20, blank=True)
    city = models.CharField('Город', max_length=100, default='Алматы')
    created = models.DateTimeField('Создан', auto_now_add=True)
    updated = models.DateTimeField('Обновлён', auto_now=True)
    paid = models.BooleanField('Оплачен', default=False)
    delivery_time = models.CharField('Желаемое время доставки', max_length=50, blank=True)
    comment = models.TextField('Комментарий к заказу', blank=True)
    delivery_price = models.DecimalField('Стоимость доставки', max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'             # ← красиво в меню
        ordering = ('-created',)

    def __str__(self):
        return f'Заказ №{self.id} — {self.first_name} {self.last_name}'

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all()) + self.delivery_price


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', verbose_name='Заказ', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', verbose_name='Товар', on_delete=models.CASCADE)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество')

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self):
        return f'{self.quantity} × {self.product.name}'

    def get_cost(self):
        return self.price * self.quantity