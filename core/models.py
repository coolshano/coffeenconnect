from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("mentor", "Mentor"),
        ("mentee", "Mentee"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.email} ({self.role})"
    

class Mentee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="mentee")
    profile_text = models.TextField()
    embedding = models.JSONField(null=True, blank=True)
    linkedin = models.URLField(blank=True, null=True)
    cv = models.FileField(upload_to="cvs/", blank=True, null=True)




class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="mentor")

    name = models.CharField(max_length=120)

    profile_text = models.TextField()
    embedding = models.JSONField(null=True, blank=True)

    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    cv = models.FileField(upload_to="cvs/", blank=True, null=True)

    def __str__(self):
        return self.name or self.user.email


class MentorRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("mentee", "mentor")
        indexes = [
            models.Index(fields=["mentor", "status"]),
            models.Index(fields=["mentee", "status"]),
        ]

    def __str__(self):
        return f"{self.mentee.user.email} → {self.mentor.user.email}"
