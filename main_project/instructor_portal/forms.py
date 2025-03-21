from django import forms

from main_page_app.models import *
from .models import *


class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["user_profile_image"]

class CourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = [
            'title', 'category', 'skill_level', 'description', 'image', 'price', 'discount',
            'duration', 'enrollment_deadline', 'prerequisites'
        ]

class SyllabusForm(forms.ModelForm):
    class Meta:
        model = CourseSyllabus
        fields = ['title', 'description']

class VideoForm(forms.ModelForm):
    class Meta:
        model = CourseVideo
        fields = ['title', 'video_url']
