# Generated by Django 4.0.10 on 2023-12-28 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0016_alter_profile_relation_formats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='relation_formats',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.relationformatsmodel'),
        ),
    ]
