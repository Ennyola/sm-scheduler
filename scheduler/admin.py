from django.contrib import admin

from .models import ScheduledPost


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
