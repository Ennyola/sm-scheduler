import os
import json
from typing import Type

from celery import shared_task
from requests_oauthlib import OAuth1Session

from django.conf import settings
from django.shortcuts import redirect

from .models import SocialMediaAccount

USER = settings.AUTH_USER_MODEL
consumer_key = os.environ.get("API_KEY")
consumer_secret = os.environ.get("API_KEY_SECRET")
# Celery tasks


@shared_task
def connect_twitter():
    request_token_url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)


def get_twitter_authorization_url() -> str:
    request_token_url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

    # Get request token
    oauth.fetch_request_token(request_token_url)

    # Get authorization url
    base_authorization_url = "https://api.twitter.com/oauth/authorize"
    authorization_url = oauth.authorization_url(base_authorization_url)
    return authorization_url


def get_twitter_access_token(user: USER, oauth_token: str, verifier: str) -> None:
    access_token_url = "https://api.twitter.com/oauth/access_token"
    request_token_url = "https://api.twitter.com/oauth/request_token"

    # oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
    # fetch_response = oauth.fetch_request_token(request_token_url)

    # resource_owner_key = fetch_response.get("oauth_token")
    # resource_owner_secret = fetch_response.get("oauth_token_secret")
    # print(resource_owner_key)
    # print(resource_owner_secret)
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=oauth_token,
        verifier=verifier,
    )
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]
    print(access_token)
    print(access_token_secret)
    # SocialMediaAccount.objects.create(
    #     user=user,
    #     platform="twitter",
    #     access_token=access_token,
    #     access_token_secret=access_token_secret,
    # )
