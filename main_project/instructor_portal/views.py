from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ProfileImageForm

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
