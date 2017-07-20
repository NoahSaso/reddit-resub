reddit-resub
============

Transfer subreddits from one Reddit account to another.

Useful when you create a new user account and want to transfer your previous subreddits over.

Environment Setup
=================

```
git clone https://github.com/NoahSaso/reddit-resub.git
cd reddit-resub
virtualenv . -p python3
source bin/activate
pip3 install -r requirements.txt
```

Usage Instructions
==================

* Go to [https://www.reddit.com/prefs/apps/](https://www.reddit.com/prefs/apps/) and press the create button
* Enter any name (`resub` is fine)
* Select `script` out of the three options (web app, installed app, script)
* `description` and `about url` don't matter and are not required (as of writing this)
* `redirect url` is required but doesn't matter, just put `https://reddit.com`
* Copy `config.ini.example` to `config.ini` and fill out your credentials
* `client_id` is the 14-character string under `personal use script`
* `client_secret` is the 27-character string next to `secret:`
* Run the command

Example:
```
python3 resub.py --extra AskReddit,announcements --nosub aww --unsub
```
This will subscribe the 'to' user in the config to all subreddits of the 'from' user PLUS /r/AskReddit and /r/announcements and EXCLUDING /r/aww. It will also unsubscribe the 'to' user from all OTHER subreddits, essentially ensuring that it is subscribed to exactly the same subreddits as the 'from' user (if a subreddit is part of the 'nosub' command, like /r/aww, the 'to' user will be unsubscribed from it).

```
usage: resub.py [-h] [-e sub1,sub2,etc.] [-n sub1,sub2,etc.] [-u] [-r]
                [-c other_config.ini] [-i]

Transfer subreddit subscriptions from one account to another.

optional arguments:
  -h, --help            show this help message and exit
  -e sub1,sub2,etc., --extra sub1,sub2,etc.
                        extra subreddits to subscribe to
  -n sub1,sub2,etc., --nosub sub1,sub2,etc.
                        don't sub to these subreddits even if in from's
                        account
  -u, --unsub           also unsub to's account from subreddits not on from's
                        account
  -r, --removesubs      remove all subs from to's account
  -c other_config.ini, --config other_config.ini
                        override config file
  -i, --interactive     enter passwords securely instead of storing them in a
                        config file
```
