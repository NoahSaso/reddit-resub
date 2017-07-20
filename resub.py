#!/usr/bin/env python3

import praw
import argparse
import configparser
import json
import getpass

parser = argparse.ArgumentParser(
    description='Transfer subreddit subscriptions from one account to another.')
parser.add_argument('-e', '--extra', help="extra subreddits to subscribe to", dest="extra", metavar="sub1,sub2,etc.")
parser.add_argument('-n', '--nosub', help="don't sub to these subreddits even if in from's account", dest="nosub", metavar="sub1,sub2,etc.", default="")
parser.add_argument('-u', '--unsub', help="also unsub to's account from subreddits not on from's account", action="store_true", dest="unsub")
parser.add_argument('-r', '--removesubs', help="remove all subs from to's account", action="store_true", dest="removesubs")
parser.add_argument('-c', '--config', help="override config file", dest="configfile", default="config.ini")
parser.add_argument('-i', '--interactive', help="enter passwords securely instead of storing them in a config file", action="store_true", dest="interactive")

class Sub:
    def __init__(self, args):
        self.args = args

        config = configparser.RawConfigParser()
        config.read(self.args.configfile)

        app = config['app']
        self.from_creds = config['from']
        self.to_creds = config['to']

        if self.args.interactive or app['interactive'].lower() in ['true', '1', 'yes']:
        	self.from_creds['username'] = input("Enter from account's username: ")
        	self.from_creds['password'] = getpass.getpass("Enter from account's password: ")

        	self.to_creds['username'] = input("Enter to account's username: ")
        	self.to_creds['password'] = getpass.getpass("Enter to account's password: ")

        	app['client_id'] = input("Enter client id: ")
        	app['client_secret'] = getpass.getpass("Enter client secret: ")

        self._r_from = praw.Reddit(user_agent='reddit-resub-from 2017-07-13', username=self.from_creds['username'], password=self.from_creds['password'], client_id=app['client_id'], client_secret=app['client_secret'])
        self._r_to = praw.Reddit(user_agent='reddit-resub-to 2017-07-13', username=self.to_creds['username'], password=self.to_creds['password'], client_id=app['client_id'], client_secret=app['client_secret'])

    def remove(self):

    	# Subs in to's account
    	to_subs = self.get_subs(self._r_to)

    	print("Removing all ({count}) subs from {to_name}".format(count=len(to_subs), to_name=self.to_creds['username']))

    	for sub in to_subs:
    		self.unsub(self._r_to, sub)
    		print("Unsubscribed from {sub} ({left} left)".format(sub=sub, left=(len(to_subs) - (to_subs.index(sub) + 1))))

    def transfer(self):

        print("Subscribing {to_name} to subs of {from_name}".format(to_name=self.to_creds['username'], from_name=self.from_creds['username']))

        # Subs in from's account
        from_subs = self.get_subs(self._r_from)
        print("Got subs of from user")
        # Add extra to subscribe to if argument passed
        if self.args.extra:
            from_subs.extend(self.args.extra.split(','))

        # Subs in to's account
        to_subs = self.get_subs(self._r_to)
        print("Got subs of to user")

        # Subscribe to subs in from's account if not already in to's account and not in nosub argument is passed
        subs_to_add = [sub for sub in from_subs if sub not in (to_subs + self.args.nosub.split(','))]
        print("Subscribing to {subs_count} subs".format(subs_count=len(subs_to_add)))
        for sub in subs_to_add:
            self.sub(self._r_to, sub)
            print("Subscribed to {sub} ({left} left)".format(sub=sub, left=(len(subs_to_add) - (subs_to_add.index(sub) + 1))))

        # Unsub from subs in to's account including the 'nosub' subs if unsub argument is passed
        if self.args.unsub:
            subs_to_del = [sub for sub in to_subs if sub not in (from_subs - self.args.nosub.split(','))]
            print("Unsubscribing from {subs_count} subs".format(subs_count=len(subs_to_del)))
            for sub in subs_to_del:
                self.unsub(self._r_to, sub)
                print("Unsubscribed from {sub} ({left} left)".format(sub=sub, left=(len(subs_to_del) - (subs_to_del.index(sub) + 1))))

    def sub(self, reddit_instance, sub):
        # Subscribe user to subreddit
        reddit_instance.subreddit(sub).subscribe()

    def unsub(self, reddit_instance, sub):
        # Unsubscribes user from subreddit
        reddit_instance.subreddit(sub).unsubscribe()

    def get_subs(self, reddit_instance):
        # Returns a list of subreddits to which the user is subscribed
        my_subs = []
        for sub in reddit_instance.user.subreddits(limit=None):
            my_subs.append(str(sub))
        return my_subs


if __name__ == "__main__":
    args = parser.parse_args()

    s = Sub(args)
    if args.removesubs:
    	s.remove()
    else:
	    s.transfer()
