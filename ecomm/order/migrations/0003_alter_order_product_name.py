# Generated by Django 4.2 on 2023-04-30 21:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_alter_order_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='product_name',
            field=models.CharField(max_length=20, validators=[django.core.validators.MinValueValidator(3)]),
        ),
    ]