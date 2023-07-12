import os
import json
from typing import Type

from celery import shared_task
from requests_oauthlib import OAuth1Session

from django.conf import settings
from django.shortcuts import redirect

USER = settings.AUTH_USER_MODEL
consumer_key = os.environ.get("API_KEY")
consumer_secret = os.environ.get("API_KEY_SECRET")
oauth = None
# Celery tasks


@shared_task
def connect_twitter():
    request_token_url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)


def get_twitter_authorization_url():
    request_token_url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
    oauth.fetch_request_token(request_token_url)
    # Get authorization
    base_authorization_url = "https://api.twitter.com/oauth/authorize"
    authorization_url = oauth.authorization_url(base_authorization_url)
    return authorization_url

