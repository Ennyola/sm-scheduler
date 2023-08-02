from django.db import models
from django.conf import settings


USER = settings.AUTH_USER_MODEL


class SocialMediaAccount(models.Model):
    PLATFORM_CHOICES = (
        ("facebook", "Facebook"),
        ("twitter", "Twitter"),
        ("instagram", "Instagram"),
        ("linkedin", "Linkedin"),
    )

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    access_token = models.CharField(max_length=255)
    access_token_secret = models.CharField(max_length=255)
    # The name attribute signifies the name set on a specific
    # social media account, which is different from your username.
    name = models.CharField(max_length=250)
    # Username on a specific social account.
    username = models.CharField(max_length=250)
    # The django user associated with this account.
    profile_picture_url = models.URLField(max_length=500)
    user = models.ForeignKey(USER, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.platform} - {self.user.username}"
