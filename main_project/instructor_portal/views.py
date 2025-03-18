from django.shortcuts import render

# Create your views here.


def instructor_dashboard(request):
    user = request.user
    return render(request, "inst_dashboard/inst_dashboard.html", {"user": user})
