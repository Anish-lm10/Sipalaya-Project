import re

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail, EmailMessage

from .models import *
from .forms import CustomUserCreationForm
from datetime import datetime


# Create your views here.
def base(request):
    user = CustomUser.objects.all()
    return render(request, "base.html", {"user": user, "date": datetime.now().year})


def home(request):
    courses = Courses.objects.filter(is_new=True, is_active=True).first()
    coursess = Courses.objects.all()[:6]
    offers = SpecialOffers.objects.filter(is_active=True)[:3]
    announcement = Announcement.objects.filter(is_active=True).first()
    testimonials = Testimonial.objects.all()
    context = {
        "courses": courses,
        "coursess": coursess,
        "offers": offers,
        "announcement": announcement,
        "testimonials": testimonials,
        "date": datetime.now().year,
    }
    return render(request, "mainpage_html/home.html", context)


def courses(request):
    courses = Courses.objects.all()
    context = {"courses": courses, "date": datetime.now().year}
    return render(request, "mainpage_html/courses.html", context)


def aboutus(request):
    return render(request, "mainpage_html/aboutus.html", {"date": datetime.now().year})


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        emails = request.POST.get("email")
        textareas = request.POST.get("textareas")

        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", emails):
            messages.error(request, "Invalid email")
            return redirect("contact")
        else:
            try:
                email_message = EmailMessage(
                    subject=name,
                    body=textareas,
                    from_email="anishnepal000@gmail.com",  # Your verified email address
                    to=["anishnepal000@gmail.com"],  # Recipient's email address
                    headers={"Reply-To": emails},  # User's email in Reply-To header
                )
                email_message.send(fail_silently=False)
                messages.success(request, "Email has been sent!!")
                return redirect("home")
            except Exception as e:
                messages.error(request, f"Error sending email: {e}")
                return redirect("contact")

    return render(request, "mainpage_html/contact.html", {"date": datetime.now().year})


def blog_list(request):
    blogs = BlogPost.objects.all().order_by("-created_at")
    return render(
        request,
        "mainpage_html/blogs.html",
        {"blogs": blogs, "date": datetime.now().year},
    )


def blog_details(request, slug):
    blog = BlogPost.objects.get(slug=slug)
    return render(
        request,
        "mainpage_html/blog_detail.html",
        {"blog": blog, "date": datetime.now().year},
    )


def policy(request):
    return render(request, "mainpage_html/policy.html", {"date": datetime.now().year})


####################################################################################
#######################---Authentication----########################################
####################################################################################
def log_in(request):
    if request.method == "POST":
        form = AuthenticationForm(
            request, data=request.POST
        )  # AuthenticationForm for login,handles authentication logic and validation.
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")

                if user.user_type == "student":
                    return redirect("home")
                elif user.user_type == "instructor":
                    return redirect("instructor_dashboard")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(
        request,
        "authentication/login.html",
        {"form": form, "date": datetime.now().year},
    )


def sign_in(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(
                commit=False
            )  # Create user but don't save to DB immediately
            user.user_type = "student"
            user.save()
            login(request, user)
            messages.success(request, "Signup successful! Welcome.")
            return redirect("home")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(
        request,
        "authentication/signup.html",
        {"form": form, "date": datetime.now().year},
    )


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")
