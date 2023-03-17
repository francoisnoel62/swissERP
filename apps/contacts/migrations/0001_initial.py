# Generated by Django 4.1.1 on 2023-03-01 15:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactsImport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='contacts')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('title', models.CharField(choices=[('Mr', 'Mister'), ('Ms', 'Madame'), ('Miss', 'Miss')], default='Mme', max_length=50, verbose_name='titre')),
                ('name', models.CharField(max_length=200, verbose_name='Prénom')),
                ('lastname', models.CharField(max_length=200, verbose_name='Nom de famille')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None)),
                ('date_of_birth', models.DateField(verbose_name='Date of birth')),
                ('street', models.CharField(max_length=100, verbose_name='Adresse')),
                ('region_zip', models.CharField(max_length=50, verbose_name='Code postale')),
                ('city', models.CharField(max_length=60, verbose_name='Ville')),
                ('country', models.CharField(max_length=50, verbose_name='Pays')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
