# Generated by Django 4.2 on 2023-05-19 19:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_order_delivered_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivered_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 22, 19, 44, 59, 217848, tzinfo=datetime.timezone.utc), editable=False),
        ),
    ]
