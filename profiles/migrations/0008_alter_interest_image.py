# Generated by Django 4.0.10 on 2023-12-21 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_alter_interest_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interest',
            name='image',
            field=models.FileField(default='interests_covers/default_interest_cover.svg', upload_to='interests_covers/'),
        ),
    ]
