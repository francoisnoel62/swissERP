# Generated by Django 3.1.6 on 2021-02-19 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_categ_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='categ_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='products.productcategory'),
            preserve_default=False,
        ),
    ]
