from django.contrib import admin
from .models import *


# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    # отображаемые поля
    list_display = ['name', 'image', 'slug', 'price', 'available', 'created', 'updated']
    # фильтры
    list_filter = ['category', 'available', 'created', 'updated']
    # можно редактировать прямо на странице
    list_editable = ['price', 'available', 'image']
    # значение автоматически устанавливается с использованием значения поля name
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ProductAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'email',
                    'address', 'delivery', 'phone', 'paid',
                    'created', 'updated','done']
    list_filter = ['paid', 'created', 'updated','done']
    inlines = [OrderItemInline]
