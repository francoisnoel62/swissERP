# Generated by Django 3.1.6 on 2021-03-02 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0003_auto_20210302_1343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saleorder',
            name='create_at',
        ),
        migrations.RemoveField(
            model_name='saleorder',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='saleorder',
            name='validity_date',
        ),
    ]
