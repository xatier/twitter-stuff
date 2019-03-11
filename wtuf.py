#!/usr/bin/env python3

from typing import List, Tuple

from tqdm import tqdm
import twitter

import utils

LOGGER = utils.get_logger(__name__)


def go(api: twitter.api.Api, start_user: str) -> Tuple[
    List[twitter.models.User], List[twitter.models.User]
]:
    # sanity check
    utils.verify(api)
    LOGGER.info(utils.get_rate_limit(api))

    friends = utils.get_friends(api, start_user)

    LOGGER.info('finding < 500 tweets accounts')
    less_than_500_tweets = sorted(
        (user for user in tqdm(friends) if user.statuses_count < 500),
        key=lambda u: u.statuses_count,
        reverse=True
    )

    LOGGER.info('finding accounts havent tweeted since 2018')
    inactive_accounts = sorted(
        (
            user for user in tqdm(friends)
            if user.status and int(user.status.created_at.split()[-1]) < 2018
        ),
        key=lambda u: u.status.created_at_in_seconds,
        reverse=True
    )

    LOGGER.info(utils.get_rate_limit(api))

    return less_than_500_tweets, inactive_accounts


def report(
    less_than_500_tweets: List[twitter.models.User],
    inactive_accounts: List[twitter.models.User],
    filename: str
) -> None:

    with open(filename, 'w') as f:

        f.write('less than 500 tweets\n')
        f.write('=' * 20 + '\n')
        for user in less_than_500_tweets:
            f.write(
                f"{user.statuses_count:<5} https://twitter.com/{user.screen_name} {user.name}\n"  # noqa
            )
        f.write('\n\n')

        f.write('inactive users since 2018\n')
        f.write('=' * 20 + '\n')
        for user in inactive_accounts:
            f.write(
                f"{user.status.created_at}   https://twitter.com/{user.screen_name} {user.name}\n"  # noqa
            )


if __name__ == '__main__':
    start_user = 'xatierlikelee'
    api = utils.login()
    less_than_500_tweets, inactive_accounts = go(api, start_user)
    report(less_than_500_tweets, inactive_accounts, f'wtuf_{start_user}.txt')
