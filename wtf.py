#!/usr/bin/env python3

import collections
from typing import Counter

from tqdm import tqdm
import twitter

import utils

LOGGER = utils.get_logger(__name__)


def go(api: twitter.api.Api, start_user: str) -> collections.Counter:
    # sanity check
    utils.verify(api)
    LOGGER.info(utils.get_rate_limit(api))

    # {'user screen name': 'count'}
    stats: Counter = collections.Counter()

    friends = utils.get_friends(api, start_user)
    LOGGER.info('%s has %d friends', start_user, len(friends))

    for u in tqdm(friends):
        LOGGER.info(
            '@%s (following %d, followers %d) => %s',
            u.screen_name, u.friends_count, u.followers_count, u.name
        )
        stats[u.screen_name] += 1

        for u2 in utils.get_friends(api, u.screen_name):
            stats[u2.screen_name] += 1

        utils.do_sleep()

    return stats


def report(stats: collections.Counter, filename: str) -> None:
    # sort user name by counter value
    users = sorted(stats.items(), key=lambda kv: kv[1], reverse=True)

    with open(filename, 'w') as f:
        for user in users:
            f.write(f"{user[1]:<5} https://twitter.com/{user[0]}\n")


if __name__ == '__main__':
    start_user = 'daddysg1rls'
    api = utils.login()
    s = go(api, start_user)
    report(s, f'wtf_{start_user}.txt')
