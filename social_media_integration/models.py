from django.db import models
from django.conf import settings


USER = settings.AUTH_USER_MODEL


class SocialMediaAccount(models.Model):
    PLATFORM_CHOICES = (
        ("facebook", "Facebook"),
        ("twitter", "Twitter"),
        ("instagram", "Instagram"),
        ("linkedin", "Linkedin")
    )

    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    access_token = models.CharField(max_length=255)
    access_token_secret = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.platform} - {self.user.username}"
