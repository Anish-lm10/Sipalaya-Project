from django.db import models


# Create your models here.

class CourseSyllabus(models.Model):
    course = models.ForeignKey('main_page_app.Courses', on_delete=models.CASCADE, related_name='syllabus')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)  # To order syllabus items

    def __str__(self):
        return self.title
    
class CourseVideo(models.Model):
    course = models.ForeignKey('main_page_app.Courses', on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)
    video_url = models.URLField()  # Link to the video (e.g., YouTube, Vimeo, or hosted)
    order = models.PositiveIntegerField(default=0)  # To order videos

    def __str__(self):
        return self.title