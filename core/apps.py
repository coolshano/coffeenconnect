from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        from django.db.models.signals import post_save
        from django.contrib.auth.models import User
        from .models import Mentor, Mentee
        from .signals import mentor_embedding, mentee_embedding, create_user_profile

        post_save.connect(create_user_profile, sender=User)
        post_save.connect(mentor_embedding, sender=Mentor)
        post_save.connect(mentee_embedding, sender=Mentee)