# Generated by Django 4.0.10 on 2023-12-28 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0012_alter_uploadedprofilepictures_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedprofilepictures',
            name='profile_uploader',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.profile'),
        ),
    ]
