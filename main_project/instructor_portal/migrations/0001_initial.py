# Generated by Django 5.1.5 on 2025-03-23 15:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main_page_app', '0014_courses_instructor'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseSyllabus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('order', models.PositiveIntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='syllabus', to='main_page_app.courses')),
            ],
        ),
        migrations.CreateModel(
            name='CourseVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('video_url', models.URLField()),
                ('order', models.PositiveIntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='main_page_app.courses')),
            ],
        ),
    ]
