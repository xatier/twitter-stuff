import json
import logging
import time
import typing

import twitter

import api_keys

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(logging.StreamHandler())


def dump(j) -> None:
    if isinstance(j, twitter.models.TwitterModel):
        j = j.AsDict()
    LOGGER.info(json.dumps(j, sort_keys=True, indent=2))


def verify(api: twitter.api.Api) -> None:
    dump(api.VerifyCredentials())


def get_rate_limit(
    api: twitter.api.Api
) -> twitter.ratelimit.EndpointRateLimit:
    return api.CheckRateLimit('https://api.twitter.com/1.1/friends/list.json')


def login() -> twitter.api.Api:
    return twitter.Api(
        consumer_key=api_keys.consumer_key,
        consumer_secret=api_keys.consumer_secret,
        access_token_key=api_keys.access_token_key,
        access_token_secret=api_keys.access_token_secret,
        sleep_on_rate_limit=True
    )


def get_friends(
    api: twitter.api.Api, screen_name: str
) -> typing.List[twitter.models.User]:
    friends = []

    try:
        friends = api.GetFriends(screen_name=screen_name)
    except twitter.error.TwitterError as e:
        LOGGER.warning('Twitter error %s, skipping %s', e, screen_name)
    except Exception as e:
        LOGGER.error('Unknown error %s, skipping %s', e, screen_name)

    return friends


def get_followers(
    api: twitter.api.Api, screen_name: str
) -> typing.List[twitter.models.User]:
    followers = []

    try:
        followers = api.GetFollowers(screen_name=screen_name)
    except twitter.error.TwitterError as e:
        LOGGER.warning('Twitter error %s, skipping %s', e, screen_name)
    except Exception as e:
        LOGGER.error('Unknown error %s, skipping %s', e, screen_name)

    return followers


def do_sleep() -> None:
    time.sleep(90)
