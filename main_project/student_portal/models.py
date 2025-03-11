from django.db import models

from main_page_app.models import *


# Enrollment Model
class Enrollment(models.Model):
    PAYMENT_STATUS = (
        ("PENDING", "pending"),
        ("Paid", "Paid"),
    )
    student = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, limit_choices_to={"user_type": "student"}
    )
    courses = models.ForeignKey(Courses, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=100, choices=PAYMENT_STATUS, default="PENDING"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.email} enrolled in {self.courses.title}"


# Assignment-Submission Model
class Assignment(models.Model):
    pass


class Submission(models.Model):
    pass


# Job-Listing Model
class JobListing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    company_name = models.CharField(max_length=255)
    job_type = models.CharField(
        max_length=50,
        choices=[
            ("full_time", "Full Time"),
            ("part_time", "Part Time"),
            ("internship", "Internship"),
            ("remote", "Remote"),
        ],
        default=True
    )
    location=models.CharField(max_length=200,null=True)
    contact_email = models.EmailField(null=True) 
    application_deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
