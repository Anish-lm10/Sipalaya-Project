import re
import uuid

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import requests


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
    courses = Courses.objects.filter(is_active=True)

    # Filters
    skill_level = request.GET.get("skill_level")
    duration = request.GET.get("duration")
    price = request.GET.get("price")

    if skill_level:
        courses = courses.filter(skill_level__iexact=skill_level)

    if duration:
        courses = courses.filter(duration__lte=duration)

    if price:
        courses = courses.filter(price__lte=price)

    context = {
        "courses": courses,
        "date": datetime.now().year,
        "selected_skill_level": skill_level,
        "selected_duration": duration,
        "selected_price": price,
    }
    return render(request, "mainpage_html/courses.html", context)


def course_detail(request, id):
    course = Courses.objects.get(id=id)
    return render(request, "mainpage_html/courses_one.html", {"course": course})


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


####################################################################################
#######################---Payment----########################################
####################################################################################


@login_required(login_url="login")
def payment_page(request, id):
    course = Courses.objects.get(id=id)
    transaction_id = uuid.uuid4().hex  # Generate a unique transaction ID

    context = {
        "course": course,
        "transaction_id": transaction_id,
    }

    return render(request, "payments/payment.html", context)


# ESEWA
def esewa_success(request):
    transaction_id = request.GET.get("transaction_uuid")
    status = request.GET.get("status")  # 'Success' or 'Failed'

    if not transaction_id:
        return render(
            request, "payments/esewa_failure.html", {"error": "Invalid transaction ID"}
        )

    try:
        # Fetch the course ID from the session
        course_id = request.session.get("course_id")
        if not course_id:
            return render(
                request, "payments/esewa_failure.html", {"error": "Course not found."}
            )

        # Fetch the course object using the course ID
        course = get_object_or_404(Courses, id=course_id)

        if status == "Completed":
            # Now create the payment record in the database
            payment = Payment.objects.create(
                user=request.user,
                course=course,
                transaction_id=transaction_id,
                amount=course.discount,
                status="Completed",  # mark as completed
            )
            return render(request, "payments/esewa_success.html", {"payment": payment})
        else:
            # If the payment failed, show failure page
            return render(
                request, "payments/esewa_failure.html", {"error": "Payment failed."}
            )

    except Exception as e:
        return render(
            request, "payments/esewa_failure.html", {"error": f"Error: {str(e)}"}
        )


def esewa_failure(request):
    return render(request, "payments/esewa_failure.html")


# khalti
KHALTI_SECRET_KEY = "4744b9a29b4e4ff496c44507683ed05c"
KHALTI_INITIATE_URL = "https://dev.khalti.com/api/v2/epayment/initiate/"


def initkhalti(request):
    if request.method == "POST":
        print(f"POST data: {request.POST}")
        purchase_order_id = request.POST.get("purchase_order_id")
        amount = int(request.POST.get("amount")) * 100  # Convert NPR to Paisa
        course_id = request.POST.get("course_id")

        # Store course_id in session to use it later
        request.session["course_id"] = course_id

        return_url = request.build_absolute_uri(reverse("khalti_success"))

        payload = {
            "return_url": return_url,
            "website_url": request.build_absolute_uri("/"),
            "amount": amount,
            "purchase_order_id": purchase_order_id,
            "purchase_order_name": "Course Payment",
        }

        headers = {"Authorization": f"Key {KHALTI_SECRET_KEY}"}

        response = requests.post(KHALTI_INITIATE_URL, json=payload, headers=headers)
        response_data = response.json()

        if response.status_code == 200 and "payment_url" in response_data:
            khalti_payment_url = response_data["payment_url"]
            return redirect(khalti_payment_url)
        else:
            return JsonResponse({"error": "Khalti Payment Failed"}, status=400)

    return redirect("courses")  # Redirect back if method is not POST


def khalti_payment_success(request):
    token = request.GET.get("pidx")  # Khalti's payment token

    if not token:
        return JsonResponse({"error": "Invalid payment details."}, status=400)

    verification_url = "https://dev.khalti.com/api/v2/epayment/lookup/"
    headers = {
        "Authorization": f"Key {KHALTI_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"pidx": token}

    try:
        response = requests.post(verification_url, headers=headers, json=payload)

        # Check if the response is valid JSON
        try:
            response_data = response.json()
            print("Khalti API Response:", response_data)  # Debugging
        except ValueError:
            return JsonResponse(
                {"error": "Invalid response from Khalti API."}, status=500
            )

        # Handle the response based on the state
        if response.status_code == 200 and response_data.get("status") == "Completed":
            # Assuming the course ID is passed through session or another method
            course_id = request.session.get("course_id")
            print(f"Retrieved course_id from session: {course_id}")  # Debugging
            if not course_id:
                return render(
                    request,
                    "payments/esewa_failure.html",
                    {"error": "Course not found in session."},
                )

            course = Courses.objects.get(id=course_id)

            # Create or update the payment record
            payment = Payment.objects.create(
                transaction_id=token,
                user=request.user,
                course=course,
                amount=course.discount,  # Assuming the course.discount contains the correct amount
                payment_method="khalti",
                status="completed",  # Mark the payment as completed
            )

            # Render the success page
            return render(request, "payments/esewa_success.html", {"payment": payment})

        else:
            return render(
                request,
                "payments/esewa_failure.html",
                {"error": "Payment verification failed."},
            )

    except requests.exceptions.RequestException as e:
        return render(
            request,
            "payments/esewa_failure.html",
            {"error": f"Request failed: {str(e)}"},
        )
    except Exception as e:
        return render(
            request,
            "payments/esewa_failure.html",
            {"error": f"An error occurred: {str(e)}"},
        )
