from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from .models import *
from .forms import CustomUserCreationForm


# Create your views here.
def base(request):
    user=CustomUser.objects.all()
    return render(request,'base.html',{"user":user})

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
    }
    return render(request, "mainpage_html/home.html", context)


def courses(request):
    courses = Courses.objects.all()
    context = {"courses": courses}
    return render(request, "mainpage_html/courses.html", context)


def aboutus(request):
    return render(request, "mainpage_html/aboutus.html")


def contact(request):
    return render(request, "mainpage_html/contact.html")


def blog_list(request):
    blogs = BlogPost.objects.all().order_by("-created_at")
    return render(request, "mainpage_html/blogs.html", {"blogs": blogs})


def blog_details(request, slug):
    blog = BlogPost.objects.get(slug=slug)
    return render(request, "mainpage_html/blog_detail.html", {"blog": blog})


def policy(request):
    return render(request, "mainpage_html/policy.html")


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
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "authentication/login.html", {"form": form})


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
            return redirect("home")  # Change to your desired redirect URL
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, "authentication/signup.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")
