# Generated by Django 4.0.10 on 2023-12-28 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0013_alter_uploadedprofilepictures_profile_uploader'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelationFormatsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Relation', max_length=64)),
                ('about', models.CharField(default='About', max_length=512)),
                ('image', models.ImageField(blank=True, upload_to='relation_formats/<django.db.models.fields.CharField>')),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='relation_formats',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.relationformatsmodel'),
        ),
    ]