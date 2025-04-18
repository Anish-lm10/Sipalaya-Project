# Generated by Django 5.1.5 on 2025-03-23 16:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructor_portal', '0001_initial'),
        ('main_page_app', '0014_courses_instructor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursevideo',
            name='course',
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('order', models.PositiveIntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='main_page_app.courses')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('video_url', models.URLField()),
                ('order', models.PositiveIntegerField(default=0)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='instructor_portal.topic')),
            ],
        ),
        migrations.DeleteModel(
            name='CourseSyllabus',
        ),
        migrations.DeleteModel(
            name='CourseVideo',
        ),
    ]
