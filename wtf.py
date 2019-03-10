#!/usr/bin/env python3

import collections
import json
import logging
import time
import typing

import twitter

import api_keys

LOGGER = logging.getLogger()
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


def do_sleep() -> None:
    time.sleep(90)


def go(api: twitter.api.Api, start_user: str) -> collections.Counter:
    # sanity check
    verify(api)
    LOGGER.info(get_rate_limit(api))

    # {'user screen name': 'count'}
    stats = collections.Counter()

    friends = get_friends(api, start_user)
    LOGGER.info('%s has %d friends', start_user, len(friends))

    for u in friends:
        LOGGER.info(
            '@%s (following %d, followers %d) => %s',
            u.screen_name, u.friends_count, u.followers_count, u.name
        )
        stats[u.screen_name] += 1

        for u2 in get_friends(api, u.screen_name):
            stats[u2.screen_name] += 1

        do_sleep()

    return stats


def report(stats: collections.Counter, filename: str) -> None:
    # sort user name by counter value
    users = sorted(stats.items(), key=lambda kv: kv[1], reverse=True)

    with open(filename, 'w') as f:
        for user in users:
            f.write(f"{user[1]:<5} https://twitter.com/{user[0]}\n")


if __name__ == '__main__':
    start_user = 'daddysg1rls'
    api = twitter.Api(
        consumer_key=api_keys.consumer_key,
        consumer_secret=api_keys.consumer_secret,
        access_token_key=api_keys.access_token_key,
        access_token_secret=api_keys.access_token_secret,
        sleep_on_rate_limit=True
    )
    s = go(api, start_user)
    report(s, f'{start_user}.txt')
