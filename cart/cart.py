from decimal import Decimal
from shop.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, qty=1, update_qty=False):
        """
        Добавляем товар в корзину или обновляем его количество
        """
        product_id = str(product.id)
        qty = int(qty)  # ← принудительно превращаем в int

        if product_id not in self.cart:
            self.cart[product_id] = {
                'qty': 0,
                'price': str(product.price),  # цена всегда строка в сессии
            }

        if update_qty:
            self.cart[product_id]['qty'] = qty
        else:
            self.cart[product_id]['qty'] += qty

        # Если количество стало 0 или меньше — удаляем товар из корзины
        if self.cart[product_id]['qty'] <= 0:
            del self.cart[product_id]

        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

    def clear(self):
        del self.session['cart']