# Generated by Django 4.1.1 on 2022-09-19 15:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sale', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('currency', models.CharField(choices=[('CHF', 'Francs Suisse'), ('EU', 'Euros')], default='CHF', max_length=50, verbose_name='Monnaie')),
                ('total', models.FloatField(verbose_name='Montant')),
                ('payment_method', models.CharField(choices=[('IBAN', 'Virement bancaire'), ('TW', 'Twint'), ('CS', 'Cash'), ('CB', 'Carte de crédit')], default='IBAN', max_length=50, verbose_name='Payment method')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Date du paiement')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('sale_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sale.saleorder')),
            ],
        ),
    ]
