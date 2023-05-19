from django.contrib import admin

from .models import ScheduledPost, SocialMediaAccount

# Register your models here.


@admin.register(ScheduledPost)
class ScheduledPostAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "social_media_account",
        "content",
        "media",
        "scheduled_time",
        "is_published",
    )


@admin.register(SocialMediaAccount)
class SocialMediaAccountAdmin(admin.ModelAdmin):
    list_display = ("user", "platform", "access_token")
