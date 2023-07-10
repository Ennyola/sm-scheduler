from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import ProcessFormView
from django.shortcuts import redirect

from .models import SocialMediaAccount
from .tasks import add


class ManageAccountsView(ListView):
    queryset = SocialMediaAccount.objects.all()
    context_object_name = "social_accounts"
    template_name = "social_media_integration/manage_accounts.html"


class AddAccountsView(View):
    template_name = "social_media_integration/add_social_accounts.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if "twitter" in request.POST:
            add.delay(34, 23)
        return redirect("social_integration:add-social-accounts")


manage_accounts = ManageAccountsView.as_view()
add_accounts_templates_view = AddAccountsView.as_view()
