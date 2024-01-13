# Generated by Django 4.2.7 on 2024-01-12 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_product_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('address', models.CharField(blank=True, max_length=250, null=True, verbose_name='Адрес')),
                ('delivery', models.CharField(max_length=20, verbose_name='Доставка')),
                ('phone', models.CharField(max_length=12, verbose_name='Моб.телефон')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Заказ создан')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Заказ обновлен')),
                ('paid', models.BooleanField(default=False, verbose_name='Заказ оплачен/не оплачен')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='store.product', verbose_name='Наименование продукта')),
            ],
        ),
    ]