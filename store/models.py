from django.db import models
from django.urls import reverse
import re
from django.core.validators import ValidationError, RegexValidator


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Категория')
    slug = models.SlugField(max_length=200)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200)
    image = models.CharField(max_length=100, blank=True, null=True, verbose_name='Картинка')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Цена')
    volume = models.CharField(max_length=50, null=True, verbose_name='Объем')
    available = models.BooleanField(default=True, verbose_name='Доступность товара')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id, self.slug])


regex = re.compile(
    r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")


def exam_mail(email):
    if re.fullmatch(regex, email) == None:
        raise ValidationError('Введите адрес в формате address@mail.ru')


class Order(models.Model):
    DELIVERY_CHOICES = [('0', 'самовывоз'), ('1', 'Советский'), ('2', 'Володарский'), ('3', 'Фокинский'),
                        ('4', 'Бежицкий')]
    name = models.CharField(max_length=50, verbose_name='Имя')
    email = models.EmailField(verbose_name='email', validators=[exam_mail])
    address = models.CharField(max_length=250, blank=True, null=True, verbose_name='Адрес')
    delivery = models.CharField(max_length=20, verbose_name='Доставка', choices=DELIVERY_CHOICES, default='0')
    phone = models.CharField(max_length=12, verbose_name='Моб.телефон',validators=[RegexValidator('[+7][0-9]{10}', message='Введите телефон в формате +7**********')])
    created = models.DateTimeField(auto_now_add=True, verbose_name='Заказ создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Заказ обновлен')
    paid = models.BooleanField(default=False, verbose_name='Заказ оплачен/не оплачен')
    braintree_id = models.CharField(max_length=150, blank=True, verbose_name='ID транзакции')
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True, verbose_name='Сумма заказа (руб)')

    class Meta:
        ordering = ('created',)
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Наименование продукта', related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
