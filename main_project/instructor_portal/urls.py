from django.urls import path


from .views import *


urlpatterns = [
    path("", instructor_dashboard, name="instructor_dashboard"),
]
