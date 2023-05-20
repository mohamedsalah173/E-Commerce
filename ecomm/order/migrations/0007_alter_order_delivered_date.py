import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_alter_order_delivered_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivered_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 23, 6, 7, 39, 584434, tzinfo=datetime.timezone.utc), editable=False),
        ),
    ]
