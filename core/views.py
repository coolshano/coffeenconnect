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
    template_name = "login.html"

    def get_success_url(self):
        if hasattr(self.request.user, "mentor"):
            return "/mentor/dashboard/"
        else:
            return "/dashboard/"

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
            return redirect("/mentor/dashboard/")
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

@login_required
def matches(request):
    mentee = request.user.mentee

    raw = match_mentors(mentee)

    requests = MentorRequest.objects.filter(mentee=mentee)
    req_map = {r.mentor_id: r.status for r in requests}

    matches = []
    for mentor, score in raw:
        matches.append({
            "mentor": mentor,
            "score": round(score * 100, 1),
            "status": req_map.get(mentor.id)  # None, pending, accepted, rejected
        })

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

@login_required(login_url="/login/")
def accept_request(request, request_id):
    r = MentorRequest.objects.get(id=request_id)
    r.status = "accepted"
    r.save()
    return redirect("/mentor/dashboard/")

@login_required(login_url="/login/")
def reject_request(request, request_id):
    r = MentorRequest.objects.get(id=request_id)
    r.status = "rejected"
    r.save()
    return redirect("/mentor/dashboard/")

@login_required(login_url="/login/")
def mentor_dashboard(request):
    mentor = request.user.mentor

    requests = MentorRequest.objects.filter(
        mentor=mentor,
        status="pending"
    )

    return render(request, "mentor_dashboard.html", {
        "mentor": mentor,
        "requests": requests
    })


