# Generated by Django 4.0.10 on 2024-01-08 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moderating', '0006_complain_decision_complain_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='complain',
            old_name='decision',
            new_name='user_block_decision',
        ),
        migrations.AddField(
            model_name='complain',
            name='decision_explanation',
            field=models.TextField(blank=True, default='Just because!'),
        ),
    ]
