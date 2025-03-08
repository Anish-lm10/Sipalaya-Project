from django.shortcuts import render


from main_page_app.models import *


# Create your views here.

def dashboard(request):
    user =request.user
    return render(request, "dashboard/dashboard.html", {"user": user})