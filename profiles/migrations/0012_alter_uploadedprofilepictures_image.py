# Generated by Django 4.0.10 on 2023-12-28 11:43

from django.db import migrations, models
import profiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_remove_profile_profile_uploaded_pictures_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedprofilepictures',
            name='image',
            field=models.ImageField(blank=True, upload_to=profiles.models.create_user_path),
        ),
    ]