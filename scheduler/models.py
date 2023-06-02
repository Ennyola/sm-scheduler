from django.db import models
from django.conf import settings

from social_media_integration.models import SocialMediaAccount

USER = settings.AUTH_USER_MODEL


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
