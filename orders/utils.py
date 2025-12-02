from decimal import Decimal

def calculate_delivery(address, total):
    zones = {
        'центр': {'min_free': Decimal('0'), 'price': Decimal('500')},
        'алмалинский': {'min_free': Decimal('1500'), 'price': Decimal('0')},
        'турксибский': {'min_free': Decimal('1000'), 'price': Decimal('300')},
        'за городом': {'min_free': Decimal('3000'), 'price': Decimal('1000')},
    }
    address_lower = address.lower()
    for zone_key, data in zones.items():
        if zone_key in address_lower:
            return Decimal('0') if total >= data['min_free'] else data['price']
    return Decimal('1000')  # По умолчанию