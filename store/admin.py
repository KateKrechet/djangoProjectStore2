from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Country)

admin.site.register(Category)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product)


class ProductAdmin(admin.ModelAdmin):
    # отображаемые поля
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    # фильтры
    list_filter = ['category', 'country', 'available', 'created', 'updated']
    # можно редактировать прямо на странице
    list_editable = ['price', 'available']
    # для указания полей, где значение автоматически устанавливается с использованием значения других полей
    prepopulated_fields = {'slug': ('name',)}
