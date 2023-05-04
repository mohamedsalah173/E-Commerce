# Generated by Django 4.2 on 2023-04-30 21:57

from django.db import migrations, models
import order.models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_order_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='product_name',
            field=models.CharField(max_length=20, validators=[order.models.validate_product_name]),
        ),
    ]