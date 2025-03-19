from django.urls import path


from .views import *


urlpatterns = [
    path("", instructor_dashboard, name="instructor_dashboard"),
     path("update-profile-image/", update_profile_image, name="update_profile_image"),
     path("instructor_profile", inst_profile, name="inst_profile"),
]
