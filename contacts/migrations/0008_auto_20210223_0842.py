# Generated by Django 3.1.6 on 2021-02-23 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0007_auto_20210222_0835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='age',
            field=models.IntegerField(null=True, verbose_name='Age'),
        ),
    ]
