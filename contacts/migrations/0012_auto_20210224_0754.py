# Generated by Django 3.1.6 on 2021-02-24 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0011_auto_20210224_0750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='lang',
            field=models.CharField(choices=[('EN', 'Anglais'), ('FR', 'Francais'), ('CH', 'Suisse'), ('RU', 'Russe'), ('IT', 'Italien')], default='US', max_length=80, verbose_name='Langue'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='title',
            field=models.CharField(choices=[('M.', 'Monsieur'), ('Mme', 'Madame'), ('Melle', 'Mademoiselle'), ('NA', 'Sans avis')], default='EN', max_length=50, verbose_name='titre'),
        ),
    ]