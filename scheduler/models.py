from django.db import models
from django.conf import settings

# Create your models here.

USER = settings.AUTH_USER_MODEL


class SocialMediaAccount(models.Model):
    PLATFORM_CHOICES = (
        ("facebook", "Facebook"),
        ("twitter", "Twitter"),
        ("instagram", "Instagram"),
        ("linkedin", "Linkedin")
        # Add more platforms as needed
    )

    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    access_token = models.CharField(max_length=255)
    # Add more fields specific to each social media platform

    def __str__(self):
        return f"{self.platform} - {self.user.username}"


class ScheduledPost(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    social_media_account = models.ForeignKey(
        SocialMediaAccount, on_delete=models.CASCADE
    )
    content = models.TextField()
    media = models.ImageField(upload_to="media/", null=True, blank=True)
    scheduled_time = models.DateTimeField()
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.content[:50]}"

    class Meta:
        ordering = ["-scheduled_time"]
