from django.contrib import admin

from .models import SocialMediaAccount


# Register your models here.
@admin.register(SocialMediaAccount)
class SocialMediaAccountAdmin(admin.ModelAdmin):
    list_display: tuple[str] = ("user", "platform", "access_token")
