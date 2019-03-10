# Twitter stuff

My collection on small things I play with Twitter API.


# Requirements

## pips

```
$ python -m venv .
$ . bin/activate

$ pip install python-twitter
```

## api_keys.py

```
consumer_key = ''
consumer_secret = ''
access_token_key = ''
access_token_secret = ''
```

# fun time

- `wtf.py`: who to follow


# Development

## flake8

```
$ pip install flake8 flake8-bugbear flake8-comprehensions flake8-docstrings pep8-naming
$ flake8 --ignore C408,D1 --show-source .
```

## yapf

```
$ pip install yapf
$ yapf --style='{dedent_closing_brackets: true, split_before_logical_operator: false}'
```
