from decimal import Decimal
from django.conf import settings
from .models import Product




class Cart(object):
    def __init__(self, request):
        # Инициализация корзины

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # если корзины нет, создаем пустую
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        # Добавление продукта в корзину или изменение его количества

        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # помечаем сессию как измененную, чтобы быть уверенными, что изменеия сохранились

        self.session.modified = True

    def remove(self, product):
        # Удаление продукта из корзины

        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def __iter__(self):

        # получение информации из бд для элементов корзины
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = int(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        # подсчет количества товаров в корзине
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # удаление корзины из сеанса
        del self.session[settings.CART_SESSION_ID]
        self.save()
