# Generated by Django 4.2 on 2023-05-20 01:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_alter_order_delivered_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivered_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 23, 1, 9, 48, 378940, tzinfo=datetime.timezone.utc), editable=False),
        ),
    ]