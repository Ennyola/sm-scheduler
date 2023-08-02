import os
import logging
from typing import Literal, Optional, Any, TypedDict

from celery import shared_task
from requests_oauthlib import OAuth1Session

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from .models import SocialMediaAccount

# logging.basicConfig(
#     level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# )
# logger: logging.Logger = logging.getLogger(__name__)

USER: type[User] = get_user_model()
consumer_key: Optional[str] = os.environ.get("API_KEY")
consumer_secret: Optional[str] = os.environ.get("API_KEY_SECRET")


class TwitterProfileInfo(TypedDict):
    """

    Args:
        TypedDict (_type_): _description_
    """

    id: str
    name: str
    username: str
    profile_image_url: str


# Celery tasks
@shared_task
def get_twitter_authorization_url() -> str:
    """Gets the authorization url for access token retrieval.

    Returns:
        str: The authorization url the page gets redirected to.
    """

    request_token_url: Literal[
        "https://api.twitter.com/oauth/request_token"
    ] = "https://api.twitter.com/oauth/request_token"
    oauth: OAuth1Session = OAuth1Session(consumer_key, client_secret=consumer_secret)

    # Fetch request token
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
def get_twitter_userprofiles(username: str) -> list[TwitterProfileInfo]:
    oauth: OAuth1Session = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=account.access_token,
        resource_owner_secret=account.access_token_secret,
    )
    profile: TwitterProfileInfo = oauth.get(
        "https://api.twitter.com/2/users/me",
        params={"user.fields": "profile_image_url,name,username"},
    ).json()
    profiles.append(profile)
    return profiles


@shared_task
def get_twitter_access_token(username: str, oauth_token: str, verifier: str) -> None:
    """Retrieves and saves the tokens to the database"""

    user = USER.objects.get(username=username)
    access_token_url: Literal[
        "https://api.twitter.com/oauth/access_token"
    ] = "https://api.twitter.com/oauth/access_token"

    # Get the access token
    oauth: OAuth1Session = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=oauth_token,
        verifier=verifier,
    )
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    
    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]

    
    if not SocialMediaAccount.objects.filter(access_token=access_token).exists():
        SocialMediaAccount.objects.create(
            user=user,
            platform="twitter",
            access_token=access_token,
            access_token_secret=access_token_secret,
        )
