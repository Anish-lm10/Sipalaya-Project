# Generated by Django 5.1.5 on 2025-02-13 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page_app', '0006_courses_is_new'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
