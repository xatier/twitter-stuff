#!/usr/bin/env python3

from typing import Callable, List, Tuple

from tqdm import tqdm
import twitter

import utils

LOGGER = utils.get_logger(__name__)


def go(api: twitter.api.Api, start_user: str) -> Tuple[
    List[twitter.models.User], List[twitter.models.User],
    List[twitter.models.User], List[twitter.models.User]
]:
    # sanity check
    utils.verify(api)
    LOGGER.info(utils.get_rate_limit(api))

    friends = utils.get_friends(api, start_user)
    followers = utils.get_followers(api, start_user)

    LOGGER.info('[friends] finding < 500 tweets accounts')
    following_less_than_500_tweets = sorted(
        (user for user in tqdm(friends) if user.statuses_count < 500),
        key=lambda u: u.statuses_count,
        reverse=True
    )

    LOGGER.info('[friends] finding accounts havent tweeted since 2018')
    following_inactive_accounts = sorted(
        (
            user for user in tqdm(friends)
            if user.status and int(user.status.created_at.split()[-1]) < 2018
        ),
        key=lambda u: u.status.created_at_in_seconds,
        reverse=True
    )

    LOGGER.info('[followers] finding < 500 tweets accounts')
    follower_less_than_500_tweets = sorted(
        (user for user in tqdm(followers) if user.statuses_count < 500),
        key=lambda u: u.statuses_count,
        reverse=True
    )

    LOGGER.info('[followers] finding < 100 followers accounts')
    follower_less_than_100_followers = sorted(
        (user for user in tqdm(followers) if user.followers_count < 100),
        key=lambda u: u.followers_count,
        reverse=True
    )

    LOGGER.info(utils.get_rate_limit(api))

    return (
        following_less_than_500_tweets, following_inactive_accounts,
        follower_less_than_500_tweets, follower_less_than_100_followers
    )


def report(
    following_less_than_500_tweets: List[twitter.models.User],
    following_inactive_accounts: List[twitter.models.User],
    follower_less_than_500_tweets: List[twitter.models.User],
    follower_less_than_100_followers: List[twitter.models.User],
    filename: str
) -> None:

    def print_details_from_list(
        title: str,
        users: List[twitter.models.User],
        get_field: Callable
    ) -> None:
        f.write(f'{title}\n')
        f.write('=' * 20 + '\n')
        for user in users:
            f.write(
                f"{get_field(user)} https://twitter.com/{user.screen_name} {user.name}\n"  # noqa: E501
            )
        f.write('\n\n')

    with open(filename, 'w') as f:

        print_details_from_list(
            '[friends] less than 500 tweets',
            following_less_than_500_tweets,
            lambda user: f"{user.statuses_count:<5}"
        )

        print_details_from_list(
            '[friends] inactive users since 2018',
            following_inactive_accounts,
            lambda user: f"{user.created_at}"
        )

        print_details_from_list(
            '[followers] less than 500 tweets',
            follower_less_than_500_tweets,
            lambda user: f"{user.statuses_count:<5}"
        )
        print_details_from_list(
            '[followers] less than 100 followers',
            follower_less_than_100_followers,
            lambda user: f"{user.followers_count:<5}"
        )


if __name__ == '__main__':
    start_user = 'xatierlikelee'
    api = utils.login()
    (
        following_less_than_500_tweets, following_inactive_accounts,
        follower_less_than_500_tweets, follower_less_than_100_followers
    ) = go(api, start_user)
    report(
        following_less_than_500_tweets, following_inactive_accounts,
        follower_less_than_500_tweets, follower_less_than_100_followers,
        f'wtuf_{start_user}.txt'
    )
