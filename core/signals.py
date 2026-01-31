from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Mentor, Mentee
from .ml import get_embedding
from django.contrib.auth.models import User
from .models import UserProfile

def mentor_embedding(sender, instance, created, **kwargs):
    if instance.profile_text and not instance.embedding:
        instance.embedding = get_embedding(instance.profile_text)
        instance.save(update_fields=["embedding"])

def mentee_embedding(sender, instance, created, **kwargs):
    if instance.profile_text and not instance.embedding:
        instance.embedding = get_embedding(instance.profile_text)
        instance.save(update_fields=["embedding"])

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)