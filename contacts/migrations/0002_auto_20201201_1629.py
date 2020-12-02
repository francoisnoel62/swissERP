# Generated by Django 3.1.3 on 2020-12-01 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='city',
            field=models.CharField(default='Inconnue', max_length=100, verbose_name='Ville'),
        ),
        migrations.AddField(
            model_name='contact',
            name='is_company',
            field=models.BooleanField(default=False, verbose_name='Is a company'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='age',
            field=models.IntegerField(default=0, verbose_name='Age'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(default='Nom', max_length=200, verbose_name='Nom du contact'),
        ),
    ]
