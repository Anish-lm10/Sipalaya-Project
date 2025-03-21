from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import *

# Create your views here.


def instructor_dashboard(request):
    user = request.user
    return render(request, "inst_dashboard/inst_dashboard.html", {"user": user})


def update_profile_image(request):
    if request.method == "POST":
        form = ProfileImageForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile image updated successfully!")
            return redirect("instructor_dashboard")  # Redirect back to dashboard
    else:
        form = ProfileImageForm(instance=request.user)

    return render(request, "inst_dashboard/update_image.html", {"form": form})


def inst_profile(request):
    user = request.user
    return render(request, "inst_dashboard/inst_profile.html", {"user": user})


def create_course(request):
    if request.method == "POST":
        course_form = CourseForm(request.POST, request.FILES)
        syllabus_form = SyllabusForm(request.POST)
        video_form = VideoForm(request.POST)

        if (
            course_form.is_valid()
            and syllabus_form.is_valid()
            and video_form.is_valid()
        ):
            course = course_form.save(commit=False)
            course.instructor = request.user
            course.save()

            syllabus = syllabus_form.save(commit=False)
            syllabus.course = course
            syllabus.save()

            video = video_form.save(commit=False)
            video.course = course
            video.save()

            return redirect("instructor_dashboard")
    else:
        course_form = CourseForm()
        syllabus_form = SyllabusForm()
        video_form = VideoForm()

    return render(
        request,
        "inst_dashboard/create_course.html",
        {
            "course_form": course_form,
            "syllabus_form": syllabus_form,
            "video_form": video_form,
        },
    )
