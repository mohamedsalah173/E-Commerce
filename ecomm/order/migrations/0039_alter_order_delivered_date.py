# Generated by Django 4.2 on 2023-05-18 04:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0038_alter_order_delivered_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivered_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 21, 4, 59, 41, 815434, tzinfo=datetime.timezone.utc), editable=False),
        ),
    ]