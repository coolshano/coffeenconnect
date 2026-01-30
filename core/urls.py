from django.urls import path
from .views import register, UserLoginView, dashboard, mentor_profile, mentee_profile, test_match, matches, request_mentor


urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path("mentor/profile/", mentor_profile, name="mentor_profile"),
    path("mentee/profile/", mentee_profile, name="mentee_profile"),
    path("test-match/", test_match, name="test_match"),
    path("matches/", matches, name="matches"),
    path("request-mentor/<int:mentor_id>/", request_mentor, name="request_mentor"),

]
