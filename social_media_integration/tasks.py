import os
import json
from typing import Type

from celery import shared_task
from requests_oauthlib import OAuth1Session

from django.conf import settings

USER = settings.AUTH_USER_MODEL
consumer_key = os.environ.get("API_KEY")
consumer_secret = os.environ.get("API_KEY_SECRET")

# Celery tasks


@shared_task
def connect_twitter():
    request_token_url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
    
def connecticut():
    request_token_url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
    print(oauth)