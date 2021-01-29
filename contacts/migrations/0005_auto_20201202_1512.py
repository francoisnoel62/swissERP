# Generated by Django 3.1.3 on 2020-12-02 15:12

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0004_merge_20201202_1512'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='is_company',
        ),
        migrations.AlterField(
            model_name='contact',
            name='age',
            field=models.IntegerField(default=0, null=True, verbose_name='Age'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='city',
            field=models.CharField(max_length=200, null=True, verbose_name='Ville'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='mobile',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(max_length=200, null=True, verbose_name='Nom et prénom du contact'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
    ]