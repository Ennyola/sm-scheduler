from django.urls import path

from .views import index

app_name="social_integration"
urlpatterns = [
    path("", index, name="add-account"),
    
]
