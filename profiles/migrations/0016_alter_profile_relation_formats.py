# Generated by Django 4.0.10 on 2023-12-28 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0015_alter_profile_relation_formats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='relation_formats',
            field=models.CharField(default='SOMETHING', max_length=255),
        ),
    ]
