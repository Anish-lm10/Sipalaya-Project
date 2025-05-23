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
            "title",
            "category",
            "skill_level",
            "description",
            "syllabus",
            "course_material",
            "image",
            "price",
            "discount",
            "duration",
            "enrollment_deadline",
            "prerequisites",
        ]
