from django.urls import path
from .views import *


urlpatterns = [
    path("", home, name="home"),
    path("base", base, name="base"),
    path("courses", courses, name="courses"),
    path("course/<int:id>", course_detail, name="course_one"),
    path("about_us", aboutus, name="aboutus"),
    path("contact", contact, name="contact"),
    path("blogs", blog_list, name="blog_list"),
    path("blogs/<slug:slug>/", blog_details, name="blog_detail"),
    path("policy", policy, name="policy"),
    path("login/", log_in, name="login"),
    path("signup/", sign_in, name="signup"),
    path("logout/", logout_view, name="logout"),
]
