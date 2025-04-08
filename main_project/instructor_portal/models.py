from django.db import models


# Create your models here.

class Topic(models.Model):
    course = models.ForeignKey('main_page_app.Courses', on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=200)  # Topic title
    description = models.TextField()  # Topic description
    order = models.PositiveIntegerField(default=0)  # Order of the topic

    def __str__(self):
        return self.title
    
class Video(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)  # Video title
    video_url = models.FileField(upload_to='course_video/')  # Video URL
    order = models.PositiveIntegerField(default=0)  # Order of the video within the topic

    def __str__(self):
        return self.title