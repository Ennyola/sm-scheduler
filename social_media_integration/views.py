from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from .models import SocialMediaAccount


def manage_accounts(request):
    social_accounts = SocialMediaAccount.objects.all()
    context = {"social_accounts": social_accounts}
    return render(request, "social_media_integration/manage_accounts.html", context)


class AddAccountsView(TemplateView):
    template_name = "social_media_integration/add_social_accounts.html"


add_accounts_templates_view = AddAccountsView.as_view()
