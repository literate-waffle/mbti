import csv
import itertools
from typing import List

import tweepy

from .api import get_default_api
from .constants import MBTI_TYPES
from .models import User
from .log import get_logger

logger = get_logger(__name__)


def build_status(status: tweepy.Status) -> dict:
    return dict(
        id=status.id,
        created_at=str(status.created_at),
        name=status.user.name,
        screen_name=status.user.screen_name,
        text=_get_text(status),
    )


def _get_text(status: tweepy.Status) -> dict:
    text = None
    truncated = status.truncated
    error = False
    if not truncated:
        text = status.text
    else:
        try:
            text = status._json["extended_tweet"]["full_text"]
        except KeyError:
            text = status.text
            error = True
    return {"value": text, "truncated": truncated, "error": error}


def fetch(
    screen_name: str, count: int = 50, api: tweepy.API = None
) -> List[dict]:
    """Fetch latest tweets of a user.

    Parameters
    ----------
    screen_name : str
        The screen name of the user.
    count : int, optional
        The maximum number of tweets to fetch.
    api : tweepy.API, optional
    """
    if api is None:
        api = get_default_api()

    logger.debug(
        {"op": "user_timeline", "screen_name": screen_name, "count": count}
    )

    for status in api.user_timeline(screen_name, count=count):
        yield build_status(status)


def from_csv(filename: str, limit: int = None, **kwargs) -> List[dict]:
    """Fetch tweets of users designated in a CSV file.

    Parameters
    ----------
    filename : str
        Path to the CSV file relative to the current working directory.
    limit : int, optional
        Limit the amount of users whose tweets are fetched.
    **kwargs : any
        Keyword arguments passed to `fetch()`.
    """
    users = []

    logger.info({"op": "read-users", "filename": filename})

    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for name, screen_name, mbti in itertools.islice(reader, limit):
            mbti = mbti.upper()
            if mbti not in MBTI_TYPES:
                raise ValueError(f"Invalid MBTI type for {screen_name}: {mbti}")
            users.append(
                User(name=name, screen_name=screen_name.strip("@"), mbti=mbti)
            )

    logger.info({"op": "read-users-done", "amount": len(users)})

    for user in users:
        for status in fetch(user.screen_name, **kwargs):
            status["mbti"] = user.mbti
            logger.debug({"op": "status-parsed", "status": status})
            yield status
