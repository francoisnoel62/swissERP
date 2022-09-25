# Generated by Django 4.1.1 on 2022-09-25 18:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('classe_sessions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='schedule',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Schedule'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='session',
            name='date',
            field=models.DateField(verbose_name='Date'),
        ),
    ]
