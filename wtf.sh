#!/usr/bin/env bash

# simple who-to-follow script with twint and jq

set -ueo pipefail

TWINT_PATH="$HOME/tmp/twint"
USERNAME="${1:-xatierlikelee}"
INPUT_JSON="a.json"
OUTPUT_JSON="b.json"

pushd "$TWINT_PATH"
source venv/bin/activate

# raw json schema sample
# Ref: https://github.com/twintproject/twint/blob/master/twint/user.py#L118
: <<END
{
  "id": 1234,
  "name": "林北 其他 1 萬個人",
  "username": "asdf",
  "bio": "blah",
  "location": "Taipei City, Taiwan",
  "url": "https://google.com",
  "join_date": "1 Feb 2019",
  "join_time": "10:00 AM",
  "tweets": 5566,
  "following": 5566,
  "followers": 5566,
  "likes": 5566,
  "media": 5566,
  "private": 0,
  "verified": 0,
  "profile_image_url": "https://pbs.twimg.com/profile_images/1162421729668431875/KBr1dsxw_400x400.jpg",
  "background_image": "https://pbs.twimg.com/profile_banners/21505514/1563737501/1500x500",
}
END

# (Optional): use --limit N here
# twint -u "$USERNAME" --limit 20 --followers --user-full --json -o "$INPUT_JSON"
twint -u "$USERNAME" --followers --user-full --json -o "$INPUT_JSON"

# - delete unuseful fields
# - select conditions
# - add twitter URL to be clickable by terminal emulators

jq 'del(.verified, .profile_image_url, .background_image)
    | select(.tweets > 500 and .media > 100)
    | .twitter_url =  "https://twitter.com/" + .username
' < "$INPUT_JSON" > "$OUTPUT_JSON"


# deactivate would result in early exit if errors happen inside
set +ueo pipefail
deactivate
popd
