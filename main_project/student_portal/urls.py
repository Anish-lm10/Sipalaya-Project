from django.urls import path


from .views import *


urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("profile", my_profile, name="myprofile"),
    path("job_listing", job_announcements, name="job_listing"),
]
