from django import forms

from main_page_app.models import CustomUser


class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["user_profile_image"]
