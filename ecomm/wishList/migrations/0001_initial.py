<<<<<<< HEAD
# Generated by Django 4.2.1 on 2023-05-20 00:19
=======
# Generated by Django 4.2 on 2023-05-20 00:23
>>>>>>> 5c5376c09d134878c0312d7e8ba63eca904adeca

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
<<<<<<< HEAD
                ('product_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='products.product')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
=======
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='products.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
>>>>>>> 5c5376c09d134878c0312d7e8ba63eca904adeca
            ],
        ),
    ]
