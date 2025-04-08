from django.http import Http404
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages


from main_page_app.models import *
from instructor_portal.models import *
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


def enrolled_courses(request):
    # Get all completed payments for the current user
    completed_payments = Payment.objects.filter(
        user=request.user, status="completed"
    ).select_related("course")
    enrolled_courses = [payment.course for payment in completed_payments]
    return render(
        request,
        "dashboard/enrolled_course.html",
        {"enrolled_courses": enrolled_courses},
    )


def course_detail(request, course_id):
    course = Courses.objects.get(id=course_id)
    topics = course.topics.all().order_by("order")

    # Get the first video of the first topic by default
    first_video = None
    if topics.exists():
        first_topic = topics.first()
        if first_topic.videos.exists():
            first_video = first_topic.videos.first()

    return render(
        request,
        "dashboard/course_detail.html",
        {"course": course, "topics": topics, "current_video": first_video},
    )


def video_detail(request, course_id, video_id):
    course = Courses.objects.get(id=course_id)
    cvideo = Video.objects.get(id=video_id)
    topics = course.topics.all().order_by("order")

    all_videos = []
    for topic in topics:
        all_videos.extend(topic.videos.all())

    # Find current video index
    current_index = None
    for i, video in enumerate(all_videos):
        if video.id == cvideo.id:
            current_index = i
            break

    return render(
        request,
        "dashboard/course_detail.html",
        {
            "course": course,
            "topics": topics,
            "current_video": video,
            
        },
    )
