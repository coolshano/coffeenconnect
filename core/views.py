from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .ml import match_mentors
from .forms import MentorProfileForm, MenteeProfileForm
from .models import UserProfile, Mentor, Mentee, MentorRequest
from django.http import HttpResponse


@login_required(login_url="/login/")
def test_match(request):
    mentee = Mentee.objects.get(user=request.user)
    matches = match_mentors(mentee)

    return HttpResponse(
        "<br>".join([f"{m.user.username}: {score:.2f}" for m, score in matches])
    )
class UserLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = False


@login_required(login_url='/login/')
def dashboard(request):
    return HttpResponse("Welcome to your dashboard")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data["role"]

            # 🔐 LOGIN the new user
            login(request, user)

            if role == "mentor":
                Mentor.objects.create(user=user, profile_text="")
                return redirect("/mentor/profile/")
            else:
                Mentee.objects.create(user=user, profile_text="")
                return redirect("/mentee/profile/")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})

@login_required(login_url="/login/")
def mentor_profile(request):
    mentor = request.user.mentor   
    
    if request.method == "POST":
        form = MentorProfileForm(request.POST, request.FILES, instance=mentor)
        if form.is_valid():
            form.save()
            return redirect("/dashboard/")
    else:
        form = MentorProfileForm(instance=mentor)

    return render(request, "mentor_profile.html", {"form": form})


@login_required(login_url="/login/")
def mentee_profile(request):
    mentee = request.user.mentee

    if request.method == "POST":
        form = MenteeProfileForm(request.POST, instance=mentee)
        if form.is_valid():
            form.save()
            return redirect("/dashboard/")
    else:
        form = MenteeProfileForm(instance=mentee)

    return render(request, "mentee_profile.html", {"form": form})



@login_required(login_url="/login/")
def matches(request):
    mentee = Mentee.objects.get(user=request.user)

    raw = match_mentors(mentee)

    matches = [
        {
            "mentor": mentor,
            "score": round(score * 100, 1)
        }
        for mentor, score in raw
    ]

    return render(request, "matches.html", {"matches": matches})


from .models import MentorRequest

@login_required(login_url="/login/")
def request_mentor(request, mentor_id):
    mentee = Mentee.objects.get(user=request.user)
    mentor = Mentor.objects.get(id=mentor_id)

    MentorRequest.objects.get_or_create(
        mentee=mentee,
        mentor=mentor
    )

    return redirect("/matches/")

