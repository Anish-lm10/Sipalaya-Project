# Generated by Django 5.1.5 on 2025-01-31 05:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_page_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courses',
            old_name='special_features',
            new_name='special_offers',
        ),
    ]
