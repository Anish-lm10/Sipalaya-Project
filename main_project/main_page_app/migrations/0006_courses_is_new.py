# Generated by Django 5.1.5 on 2025-02-13 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page_app', '0005_announcement'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='is_new',
            field=models.BooleanField(default=True),
        ),
    ]
