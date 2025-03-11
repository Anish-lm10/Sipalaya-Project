from django.shortcuts import render


from main_page_app.models import *
from .models import *


# Create your views here.

def dashboard(request):
    user =request.user
    return render(request, "dashboard/dashboard.html", {"user": user})

def my_profile(request):
    user =request.user
    return render(request, "dashboard/profile.html", {"user": user})

def job_announcements(request):
    active_jobs = JobListing.objects.filter(is_active=True)
    return render(request, 'dashboard/joblisting.html', {'jobs': active_jobs})