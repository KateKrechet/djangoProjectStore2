from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны -Производители'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200)
    image = models.CharField(max_length=100, blank=True, null=True, verbose_name='Картинка')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    available = models.BooleanField(default=True, verbose_name='Доступность товара')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name
