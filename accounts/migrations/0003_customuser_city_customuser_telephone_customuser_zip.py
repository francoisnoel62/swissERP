# Generated by Django 4.1.1 on 2022-09-19 16:30

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_street'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='city',
            field=models.CharField(default=2014, max_length=55),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='telephone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None),
        ),
        migrations.AddField(
            model_name='customuser',
            name='zip',
            field=models.IntegerField(default=2555, verbose_name='zip code'),
            preserve_default=False,
        ),
    ]
