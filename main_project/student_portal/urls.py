from django.urls import path


from .views import *


urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("profile", my_profile, name="myprofile"),
    path("job_listing", job_announcements, name="job_listing"),
    path("enrolled_courses", enrolled_courses, name="enrolled_courses"),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('course/<int:course_id>/video/<int:video_id>/', video_detail, name='video_detail'),
]
