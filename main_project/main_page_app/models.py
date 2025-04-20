from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser


# User Model
class CustomUser(AbstractUser):
    USER_TYPE = (
        ("student", "Student"),
        ("instructor", "Instructor"),
    )
    user_type = models.CharField(max_length=100, choices=USER_TYPE, default="student")
    user_profile_image = models.ImageField(upload_to="images/profile_images/")
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username


# Special Offer model
class SpecialOffers(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    discount_percentage = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.discount_percentage}% off)"


# Announcement Model
class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


# Courses model
class Courses(models.Model):
    CATEGORY_CHOICES = [
        ("programming", "Programming"),
        ("web development", "Web Development"),
        ("data science & analytics", "Data Science & Analytics"),
        ("graphic designing", "Graphic Designing"),
    ]
    SKILL_LEVEL = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    skill_level = models.CharField(max_length=100, choices=SKILL_LEVEL)
    description = models.TextField()
    syllabus = models.TextField(null=True)
    course_material = models.FileField(
        upload_to="course_materials/", blank=True, null=True
    )
    image = models.ImageField(upload_to="images/courses/", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.PositiveIntegerField(default=0)
    instructor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"user_type": "instructor"},
        null=True,
    )
    duration = models.CharField(
        max_length=50, help_text="in months"
    )  # duration like 3 months
    enrollment_deadline = models.DateField()
    prerequisites = models.TextField(
        blank=True, null=True
    )  # (e.g., "Basic understanding of programming").
    special_offers = models.ManyToManyField(SpecialOffers, blank=True)
    course_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    is_new = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# Testimonial Model
class Testimonial(models.Model):
    student_name = models.CharField(max_length=100)
    postion = models.CharField(max_length=100)
    testimonial = models.TextField()
    photo = models.ImageField(upload_to="images/testimonials/", null=True, blank=True)
    rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=0.0
    )  # Max 5.0 rating
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.student_name


# Blogs Model
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    blog_image = models.ImageField(
        upload_to="images/blog_images/", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# Payment Model
class Payment(models.Model):
    PAYMENT_METHODS = [("esewa", "eSewa"), ("khalti", "Khalti")]
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, unique=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.payment_method} - {self.status}"
