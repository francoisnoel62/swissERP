# Generated by Django 4.1.1 on 2023-04-07 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classe_sessions', '0005_rename_session_presence_session_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='presence',
            old_name='uptated_at',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='session',
            old_name='updtated_at',
            new_name='updated_at',
        ),
    ]
