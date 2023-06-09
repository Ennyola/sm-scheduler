from django.urls import path

from .views import manage_accounts, add_accounts_templates_view

app_name = "social_integration"
urlpatterns = [
    path("", manage_accounts, name="manage-accounts"),
    path("add-social-account/", add_accounts_templates_view, name="add-social-accounts"),
]
