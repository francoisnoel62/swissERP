# Generated by Django 4.1.1 on 2022-09-09 16:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50, verbose_name='Nom du produit')),
                ('price', models.FloatField(verbose_name='Prix du produit')),
                ('description', models.TextField(null=True, verbose_name='Description du produit')),
                ('picture', models.ImageField(upload_to='images', verbose_name='Illustrations')),
                ('finished', models.BooleanField(default=True, verbose_name='Etat')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]