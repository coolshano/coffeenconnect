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
from django.shortcuts import get_object_or_404, redirect


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
        user = self.request.user

        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={"role": "mentee"}
        )

        if profile.role == "mentor":
            return "/mentor/dashboard/"
        else:
            return "/mentee/dashboard/"

@login_required(login_url='/login/')
def dashboard(request):
    return HttpResponse("Welcome to your dashboard")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            role = form.cleaned_data["role"]
            interested = form.cleaned_data["interested_field"]

            # Update the auto-created profile
            UserProfile.objects.filter(user=user).update(
                phone_number=form.cleaned_data["phone_number"],
                role=role,
                interested_field=interested
            )

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
    mentee, _ = Mentee.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = MenteeProfileForm(request.POST, request.FILES, instance=mentee)
        if form.is_valid():
            form.save()
            return redirect("/mentee/dashboard/")
    else:
        form = MenteeProfileForm(instance=mentee)

    return render(request, "mentee_profile.html", {"form": form})


@login_required
def matches(request):
    # Ensure user is a mentee
    try:
        mentee = request.user.mentee
    except:
        return redirect("/dashboard/")

    # Enforce completed profile
    if not mentee.profile_text or not mentee.cv:
        return redirect("/mentee/profile/")

    # Run AI matching
    raw = match_mentors(mentee)

    # Fetch existing requests
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

    return redirect("/mentee/dashboard/")

@login_required
def accept_request(request, request_id):
    req = get_object_or_404(MentorRequest, id=request_id, mentor=request.user.mentor)
    req.status = "accepted"
    req.save()
    return redirect("/mentor/dashboard/")


@login_required
def reject_request(request, request_id):
    req = get_object_or_404(MentorRequest, id=request_id, mentor=request.user.mentor)
    req.status = "rejected"
    req.save()
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


@login_required
def mentee_dashboard(request):
    mentee, _ = Mentee.objects.get_or_create(user=request.user)
    # get ML matches
    raw_matches = match_mentors(mentee)

    # existing requests
    requests = MentorRequest.objects.filter(mentee=mentee)
    req_map = {r.mentor_id: r.status for r in requests}

    mentors = []
    for mentor, score in raw_matches:
        mentors.append({
            "mentor": mentor,
            "score": round(score * 100, 1),
            "status": req_map.get(mentor.id)  # None / pending / accepted
        })

    return render(request, "mentee_dashboard.html", {
        "mentee": mentee,
        "mentors": mentors
    })



