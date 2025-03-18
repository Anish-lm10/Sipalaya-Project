from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages


from main_page_app.models import *
from .models import *


# Create your views here.


def dashboard(request):
    user = request.user
    if request.method == "POST":
        subject = "Instructor Application"
        message = f"User {user.username} has applied to become an instructor."
        from_email = "anishnepal000@gmail.com"
        recipient_list = [
            "anishnepal000@gmail.com",
        ]

        send_mail(subject, message, from_email, recipient_list)

        # Set session variable to indicate application submission
        request.session["instructor_application_submitted"] = True

    return render(request, "dashboard/dashboard.html", {"user": user})


def my_profile(request):
    user = request.user
    return render(request, "dashboard/profile.html", {"user": user})


def job_announcements(request):
    active_jobs = JobListing.objects.filter(is_active=True)
    return render(request, "dashboard/joblisting.html", {"jobs": active_jobs})
