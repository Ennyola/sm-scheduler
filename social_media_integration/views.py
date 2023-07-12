from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import ProcessFormView
from django.shortcuts import redirect

from .models import SocialMediaAccount
from .tasks import connect_twitter, get_twitter_authorization_url


class ManageAccountsView(ListView):
    queryset = SocialMediaAccount.objects.all()
    context_object_name = "social_accounts"
    template_name = "social_media_integration/manage_accounts.html"
        
    
class AddAccountsView(View):
    template_name = "social_media_integration/add_social_accounts.html"

    def get(self, request, *args, **kwargs):
        twitter_oauth_verifier = kwargs.get("oauth_verifier", None)
        
        # If no request has been made to any endpoint.
        if twitter_oauth_verifier is None:
            return render(request, self.template_name)
        # Get the twitter oauth verifier
        oauth_verifier = self.request.GET.get('oauth_verifier')
        print(oauth_verifier)
        

    def post(self, request, *args, **kwargs):
        if "twitter" in request.POST:
           authorization_url = get_twitter_authorization_url()
           print(authorization_url)
           return redirect(authorization_url)
        return redirect("social_integration:add-social-accounts")


manage_accounts = ManageAccountsView.as_view()
add_accounts_templates_view = AddAccountsView.as_view()
