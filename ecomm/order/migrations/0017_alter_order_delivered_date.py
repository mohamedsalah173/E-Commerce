# Generated by Django 4.2 on 2023-05-15 20:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_order_delivered_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivered_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 18, 20, 53, 27, 651829, tzinfo=datetime.timezone.utc)),
        ),
    ]
