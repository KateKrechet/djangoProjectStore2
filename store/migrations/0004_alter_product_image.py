# Generated by Django 4.2.7 on 2023-11-24 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_country_options_alter_product_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Картинка'),
        ),
    ]
