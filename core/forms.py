from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Mentor, Mentee

class RegisterForm(UserCreationForm):

    ROLE_CHOICES = [
        ("mentee", "Mentee"),
        ("mentor", "Mentor"),
    ]

    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15)
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = [
            "email",
            "phone_number",
            "role",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)

        # Email is username
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user
    


class MentorProfileForm(forms.ModelForm):
    class Meta:
        model = Mentor
        fields = [
            "name",
            "profile_text",
            "profile_image",
            "linkedin",
            "github",
            "cv",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Your full name",
                "class": "input"
            }),
            "profile_text": forms.Textarea(attrs={
                "placeholder": "Describe your experience, skills, and what you can mentor...",
                "rows": 6,
                "class": "textarea"
            }),
            "linkedin": forms.URLInput(attrs={
                "placeholder": "LinkedIn profile URL (optional)",
                "class": "input"
            }),
            "github": forms.URLInput(attrs={
                "placeholder": "GitHub profile URL (optional)",
                "class": "input"
            }),
            "profile_image": forms.ClearableFileInput(attrs={
                "class": "file-input",
                "data-show-current": "false"
            }),
            "cv": forms.ClearableFileInput(attrs={
                "class": "file-input",
                "data-show-current": "false"
            }),
        }

class MenteeProfileForm(forms.ModelForm):
    class Meta:
        model = Mentee
        fields = ["profile_text"]

        widgets = {
            "profile_text": forms.Textarea(attrs={
                "placeholder": "Describe your goals, background, and what help you want...",
                "rows": 6
            })
        }
