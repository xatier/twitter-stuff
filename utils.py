import datetime
import functools
import json
import logging
import time
from typing import Any, List, Tuple

import twitter

import api_keys


def get_logger(name: str) -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )
    return logging.getLogger(name)


LOGGER = get_logger(__name__)


def dump(j: Any) -> None:
    if isinstance(j, twitter.models.TwitterModel):
        j = j.AsDict()
    LOGGER.info(json.dumps(j, sort_keys=True, indent=2))


def verify(api: twitter.api.Api) -> None:
    dump(api.VerifyCredentials())


def get_rate_limit(
    api: twitter.api.Api
) -> Tuple[twitter.ratelimit.EndpointRateLimit, str]:
    r = api.CheckRateLimit('https://api.twitter.com/1.1/friends/list.json')
    return r, datetime.datetime.fromtimestamp(r.reset).ctime()


def login() -> twitter.api.Api:
    return twitter.Api(
        consumer_key=api_keys.consumer_key,
        consumer_secret=api_keys.consumer_secret,
        access_token_key=api_keys.access_token_key,
        access_token_secret=api_keys.access_token_secret,
        sleep_on_rate_limit=True
    )


@functools.lru_cache(maxsize=1024)
def get_friends(
    api: twitter.api.Api, screen_name: str
) -> List[twitter.models.User]:
    friends: List[twitter.models.User] = []

    try:
        friends = api.GetFriends(screen_name=screen_name)
    except twitter.error.TwitterError as e:
        LOGGER.warning('Twitter error %s, skipping %s', e, screen_name)
    except Exception as e:
        LOGGER.error('Unknown error %s, skipping %s', e, screen_name)

    return friends  # noqa: R504


@functools.lru_cache(maxsize=1024)
def get_followers(
    api: twitter.api.Api, screen_name: str
) -> List[twitter.models.User]:
    followers: List[twitter.models.User] = []

    try:
        followers = api.GetFollowers(screen_name=screen_name)
    except twitter.error.TwitterError as e:
        LOGGER.warning('Twitter error %s, skipping %s', e, screen_name)
    except Exception as e:
        LOGGER.error('Unknown error %s, skipping %s', e, screen_name)

    return followers  # noqa: R504


def do_sleep() -> None:
    time.sleep(75)
