# Generated by Django 4.2 on 2023-05-07 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_remove_product_category_product_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]