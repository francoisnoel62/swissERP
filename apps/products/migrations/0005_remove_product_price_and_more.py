# Generated by Django 4.1.1 on 2023-04-16 10:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_product_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='classes_by_month',
        ),
        migrations.AddField(
            model_name='subscription',
            name='classes_by_week',
            field=models.IntegerField(default=1, verbose_name='Nombre de cours par semaine'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='date_of_subscription',
            field=models.DateField(default=django.utils.timezone.now, verbose_name="Date d'abonnement"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='recurrence',
            field=models.CharField(choices=[(1, 'Mensuel'), (2, 'Annuel')], default=1, max_length=100, verbose_name='Récurrence'),
        ),
        migrations.AddField(
            model_name='unitpass',
            name='date_of_buy',
            field=models.DateField(default=django.utils.timezone.now, verbose_name="Date d'achat"),
            preserve_default=False,
        ),
    ]