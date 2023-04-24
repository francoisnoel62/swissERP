# Generated by Django 4.1.1 on 2023-04-24 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='city',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='Ville'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='country',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Pays'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='Date of birth'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='region_zip',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Code postale'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='street',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Adresse'),
        ),
    ]
