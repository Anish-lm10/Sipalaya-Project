from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser

# The form inherits from UserCreationForm so we get password validation and two password fields automatically.
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=10)

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "password1",
            "password2",
        )
