# Generated by Django 4.1.1 on 2023-04-03 14:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaleOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('validity_date', models.DateField(blank=True, null=True, verbose_name='Validity date')),
                ('order_state', models.CharField(choices=[('DR', 'Draft'), ('CL', 'Cleaned'), ('CF', 'Confirmed'), ('SD', 'Send'), ('PD', 'Paid')], default='DR', max_length=10, verbose_name='Etat de la commande')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('partner_id', models.ForeignKey(limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.PROTECT, to='contacts.contact', verbose_name='Customer')),
            ],
        ),
        migrations.CreateModel(
            name='SaleOrderLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('quantity', models.FloatField(default=1, verbose_name='Quantity')),
                ('sol_total', models.FloatField(max_length=100, verbose_name='Total')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.product', verbose_name='Products')),
                ('sale_order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sale.saleorder')),
            ],
        ),
    ]
