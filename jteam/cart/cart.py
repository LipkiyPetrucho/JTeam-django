from decimal import Decimal

from django.conf import settings

from location.models import Place


class Cart:
    def __init__(self, request):
        """Инициализировать корзину."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохранить пустую корзину в сеансе
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, place, quantity=1, override_quantity=False):
        """ Добавить место в корзину либо обновить его количество."""
        place_id = str(place.id)
        if place_id not in self.cart:
            self.cart[place_id] = {'quantity': 0,
                                   'price': str(place.price)}
        if override_quantity:
            # обновит количество товара в корзине,
            # а не будет прибавлять его к текущему количеству.
            self.cart[place_id]['quantity'] = quantity
        else:
            # прибавлять его к текущему количеству
            self.cart[place_id]['quantity'] += quantity
        self.save()

    def save(self):
        # пометить сеанс как "измененный",
        # чтобы обеспечить его сохранение
        self.session.modified = True

    def remove(self, place):
        """Удалить место из корзины."""
        place_id = str(place.id)
        if place_id in self.cart:
            del self.cart[place_id]
            self.save()

    def __iter__(self):
        """
        Прокрутить товарные позиции корзины в цикле и
        получить места из базы данных.
        """
        place_ids = self.cart.keys()
        # получить объекты place и добавить их в корзину
        places = Place.objects.filter(id__in=place_ids)
        cart = self.cart.copy()
        for place in places:
            cart[str(place.id)]['place'] = place
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Подсчитать все товарные позиции в корзине."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Расчёт общей стоимости товаров в корзине."""
        return sum(Decimal(item['price']) * item['quantity']
                   for item in self.cart.values())

    def clear(self):
        # удалить корзину из сеанса
        del self.session[settings.CART_SESSION_ID]
        self.save()
