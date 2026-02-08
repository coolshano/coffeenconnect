from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Mentor, Mentee
from .widget import CleanFileInput

INTERESTED_FIELD_CHOICES = [
    ("psychology", "Psychology"),
    ("medical", "Medical"),
    ("technology", "Technology"),
]



class RegisterForm(UserCreationForm):

    ROLE_CHOICES = [
        ("mentee", "Mentee"),
        ("mentor", "Mentor"),
    ]

    FIELD_CHOICES = [
        ("Psychology", "Psychology"),
        ("Medical", "Medical"),
        ("Technology", "Technology"),
    ]

    Education_CHOICES = [
        ("Diploma", "Diploma"),
        ("Degree", "Degree"),
        ("Masters", "Masters"),
        ("PHD", "PHD"),
    ]

    interested_field = forms.ChoiceField(choices=FIELD_CHOICES)


    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15)

    interested_field = forms.ChoiceField(
        choices=INTERESTED_FIELD_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    role = forms.ChoiceField(choices=ROLE_CHOICES)

    education = forms.ChoiceField(choices=Education_CHOICES)

    class Meta:
        model = User
        fields = [
            "email",
            "phone_number",
            "interested_field",
            "education",
            "role",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("This email is already registered.")

        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        email = self.cleaned_data["email"].lower()
        user.username = email
        user.email = email

        if commit:
            user.save()

        return user

    


class MentorProfileForm(forms.ModelForm):

    class Meta:
        model = Mentor
        fields = [
            "name", "country", "profile_text",
            "profile_image", "linkedin", "github", "cv"
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Your full name"
            }),

            "country": forms.TextInput(attrs={
                "placeholder": "Your country"
            }),

            "profile_text": forms.Textarea(attrs={
                "placeholder": "Describe your background, goals, and what you want to learn...",
                "rows": 6
            }),

            # 🔥 This removes the URLs, Clear checkbox, etc
            "profile_image": forms.FileInput(attrs={
                "class": "file-input"
            }),

            "cv": forms.FileInput(attrs={
                "class": "file-input"
            }),

            "linkedin": forms.URLInput(attrs={
                "placeholder": "LinkedIn profile (optional)"
            }),

            "github": forms.URLInput(attrs={
                "placeholder": "GitHub profile (optional)"
            }),

            }
            


class MenteeProfileForm(forms.ModelForm):
    class Meta:
        model = Mentee
        fields = [
            "name",
            "country",
            "profile_text",
            "profile_image",
            "linkedin",
            "github",
            "cv",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Your full name"
            }),

            "country": forms.TextInput(attrs={
                "placeholder": "Your country"
            }),

            "profile_text": forms.Textarea(attrs={
                "placeholder": "Describe your background, goals, and what you want to learn...",
                "rows": 6
            }),

            # 🔥 This removes the URLs, Clear checkbox, etc
            "profile_image": forms.FileInput(attrs={
                "class": "file-input"
            }),

            "cv": forms.FileInput(attrs={
                "class": "file-input"
            }),

            "linkedin": forms.URLInput(attrs={
                "placeholder": "LinkedIn profile (optional)"
            }),

            "github": forms.URLInput(attrs={
                "placeholder": "GitHub profile (optional)"
            }),
        }


