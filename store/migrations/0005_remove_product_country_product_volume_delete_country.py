# Generated by Django 4.2.7 on 2023-11-24 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='country',
        ),
        migrations.AddField(
            model_name='product',
            name='volume',
            field=models.CharField(max_length=50, null=True, verbose_name='Объем'),
        ),
        migrations.DeleteModel(
            name='Country',
        ),
    ]
