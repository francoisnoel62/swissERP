# Generated by Django 4.2 on 2023-05-02 11:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50, verbose_name='Nom du produit')),
                ('student', models.ForeignKey(blank=True, limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='contacts.contact', verbose_name='Élève')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.product')),
                ('classes_by_week', models.IntegerField(default=1, verbose_name='Cours par semaine')),
                ('date_of_subscription', models.DateField(verbose_name="Date d'abonnement")),
                ('recurrence', models.CharField(choices=[('M', 'Mensuel'), ('A', 'Annuel')], max_length=100, verbose_name='Récurrence')),
                ('current_credits', models.IntegerField(default=0, verbose_name='Crédits restants')),
            ],
            options={
                'abstract': False,
            },
            bases=('products.product',),
        ),
        migrations.CreateModel(
            name='UnitPass',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.product')),
                ('remaining_classes', models.IntegerField(default=10, verbose_name='Nombre de cours restants')),
                ('date_of_buy', models.DateField(verbose_name="Date d'achat")),
            ],
            options={
                'abstract': False,
            },
            bases=('products.product',),
        ),
    ]
