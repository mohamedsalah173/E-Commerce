# Generated by Django 4.2 on 2023-05-21 01:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_alter_order_delivered_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='delivered_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 24, 1, 0, 8, 286574, tzinfo=datetime.timezone.utc), editable=False),
        ),
    ]
