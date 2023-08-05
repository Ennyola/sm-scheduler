import os
import logging
from typing import Literal, Optional, Any, TypedDict
from dataclasses import dataclass

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
CONSUMER_KEY: Optional[str] = os.environ.get("API_KEY")
CONSUMER_SECRET: Optional[str] = os.environ.get("API_KEY_SECRET")


@dataclass
class TwitterProfileInfo:
    """A dataclass containing fields derived when an api request is made to get twitter user profile"""

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
    oauth: OAuth1Session = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_SECRET)

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
def get_twitter_userprofile(
    username: str, access_token: str, access_token_secret: str
) -> None:
    """Retrieves the user's twitter info and saves it to the database
    Args:
        username (str): The django username of the user making the request
        access_token (str): _description_
        access_token_secret (str): _description_
    """

    user = USER.objects.get(username=username)
    oauth: OAuth1Session = OAuth1Session(
        CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )
    # Fetch twitter user profile
    response = oauth.get(
        "https://api.twitter.com/2/users/me",
        params={"user.fields": "profile_image_url,name,username"},
    ).json()
    profile: TwitterProfileInfo = TwitterProfileInfo(
        name=response["data"]["name"],
        username=response["data"]["username"],
        profile_image_url=response["data"]["profile_image_url"],
    )
    if not SocialMediaAccount.objects.filter(access_token=access_token).exists():
        SocialMediaAccount.objects.create(
            user=user,
            platform="twitter",
            access_token=access_token,
            access_token_secret=access_token_secret,
            name=profile.name,
            username=profile.username,
            profile_picture_url=profile.profile_image_url,
        )


@shared_task
def get_twitter_access_token(username: str, oauth_token: str, verifier: str) -> None:
    """Retrieves and saves the tokens to the database"""

    access_token_url: Literal[
        "https://api.twitter.com/oauth/access_token"
    ] = "https://api.twitter.com/oauth/access_token"

    # Get the access token
    oauth: OAuth1Session = OAuth1Session(
        CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        resource_owner_key=oauth_token,
        verifier=verifier,
    )
    oauth_tokens = oauth.fetch_access_token(access_token_url)

    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]

    # Retrieves the user's twitter info and saves it to the database.
    get_twitter_userprofile.delay(username, access_token, access_token_secret)
