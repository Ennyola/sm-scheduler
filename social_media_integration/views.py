from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "social_media_integration/social_integration.html")