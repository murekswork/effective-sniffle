# Generated by Django 4.0.10 on 2023-12-19 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='account',
            new_name='user',
        ),
    ]
