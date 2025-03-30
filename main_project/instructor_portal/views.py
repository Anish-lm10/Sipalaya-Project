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
        if course_form.is_valid():
            # Save the course and set the instructor
            course = course_form.save(commit=False)
            course.instructor = request.user
            course.is_active = False
            course.save()

            # Save topics and videos
            topics = request.POST.getlist("topics[]")
            for i, topic_title in enumerate(topics):
                topic = Topic.objects.create(
                    course=course,
                    title=topic_title,
                    description=request.POST.getlist(f"topic_descriptions[]")[i],
                    order=i + 1,
                )

                # Save videos for this topic
                video_titles = request.POST.getlist(f"videos[{i}][title]")
                video_urls = request.POST.getlist(f"videos[{i}][url]")
                for j, video_title in enumerate(video_titles):
                    Video.objects.create(
                        topic=topic,
                        title=video_title,
                        video_url=video_urls[j],
                        order=j + 1,
                    )

            return redirect("instructor_dashboard")
    else:
        course_form = CourseForm()

    return render(
        request,
        "inst_dashboard/create_course.html",
        {
            "course_form": course_form,
        },
    )


def my_course(request):
    courses = Courses.objects.filter(instructor=request.user)
    return render(request, "inst_dashboard/mycourse.html", {"courses": courses})


# def view_course(request,pk):
#     course = Courses.objects.filter(id=pk)
#     return render(request, "inst_dashboard/view_course.html", {"course": course})
