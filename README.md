# Twitter stuff

My collection on small things I play with Twitter API.


# Requirements

## pips

- [python-twitter](https://github.com/bear/python-twitter)

```
$ python -m venv venv
$ . venv/bin/activate

$ pip install -r requirements.txt
```

## api_keys.py

- [Create an app](https://developer.twitter.com/en/apps)
- [Rate limits](https://developer.twitter.com/en/docs/basics/rate-limits)

```
consumer_key = ''
consumer_secret = ''
access_token_key = ''
access_token_secret = ''
```

# fun time

- `wtf.py`: who to follow
- `wtuf.py`: who to unfollow


# Development

- PRs are very very welcome!

## flake8

```
$ pip install flake8 flake8-bugbear flake8-comprehensions flake8-docstrings pep8-naming
$ flake8 --ignore C408,D1 --show-source *.py
```

## yapf

- yapf can't really handle python3 type annotations though. :(

```
$ pip install yapf
$ yapf --style='{dedent_closing_brackets: true, split_before_logical_operator: false}'
```

## pre-commit

```
# install pre-commit framework into git hooks
$ pip install pre-commit

# run pre-commit on all files
$ pre-commit run -a

# pull the latest repos' versions
$ pre-commit autoupdate

# cleanup
$ pre-commit gc
$ pre-commit clean
```
