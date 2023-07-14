import os
import logging

from celery import shared_task
from requests_oauthlib import OAuth1Session
from requests_oauthlib.oauth1_session import TokenRequestDenied

from django.contrib.auth import get_user_model

from .models import SocialMediaAccount

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
USER = get_user_model()
consumer_key = os.environ.get("API_KEY")
consumer_secret = os.environ.get("API_KEY_SECRET")
# Celery tasks


@shared_task
def get_twitter_authorization_url() -> str:
    """Gets the authorization url for access token retrieval.

    Returns:
        str: The authorization url the page gets redirected to.
    """
    request_token_url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

    # Fetch reqyest token
    try:
        oauth.fetch_request_token(request_token_url)
    except ValueError:
        print(
            "There may have been an issue with the consumer_key or consumer_secret you entered."
        )

    # Get authorization url
    base_authorization_url = "https://api.twitter.com/oauth/authorize"
    authorization_url = oauth.authorization_url(base_authorization_url)
    return authorization_url


@shared_task
def get_twitter_access_token(username: str, oauth_token: str, verifier: str) -> None:
    """Retrieves and saves the tokens to the database"""

    access_token_url = "https://api.twitter.com/oauth/access_token"
    user = USER.objects.get(username=username)
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=oauth_token,
        verifier=verifier,
    )
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    logger.info(oauth_tokens)
    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]
    SocialMediaAccount.objects.create(
        user=user,
        platform="twitter",
        access_token=access_token,
        access_token_secret=access_token_secret,
    )
