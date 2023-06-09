from django.shortcuts import render

from .models import SocialMediaAccount


def manage_accounts(request):
    social_accounts = SocialMediaAccount.objects.all()
    context = {"social_accounts": social_accounts}
    return render(request, "social_media_integration/manage_accounts.html", context)

def add_accounts(request):
    return render(request,"social_media_integration/add_social_accounts.html")
