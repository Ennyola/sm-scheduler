from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import SocialMediaAccount
from .tasks import (
    get_twitter_authorization_url,
    get_twitter_access_token,
)


class ManageAccountsView(ListView):
    queryset = SocialMediaAccount.objects.all()
    context_object_name = "social_accounts"
    template_name = "social_media_integration/manage_accounts.html"


class AddAccountsView(View):
    template_name = "social_media_integration/add_social_accounts.html"

    def get(self, request, *args, **kwargs):
        twitter_oauth_verifier = request.GET.get("oauth_verifier", None)
        twitter_oauth_token = request.GET.get("oauth_token", None)
        username = request.user.username
        # If no request has been made to any endpoint.
        if twitter_oauth_verifier is None:
            return render(request, self.template_name)

        # Get the twitter oauth verifier
        get_twitter_access_token.delay(
            username, twitter_oauth_token, twitter_oauth_verifier
        )
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if "twitter" in request.POST:
            authorization_url_async_result = get_twitter_authorization_url.delay()
            authorization_url = authorization_url_async_result.get()
            return redirect(authorization_url)
        return redirect("social_integration:add-social-accounts")


manage_accounts = login_required(ManageAccountsView.as_view())
add_accounts_templates_view = login_required(AddAccountsView.as_view())
