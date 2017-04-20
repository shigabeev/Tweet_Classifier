 #!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv

# tweepy.org
import tweepy
import config
# Get your Twitter API credentials and enter them here
consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_key = config.access_key
access_secret = config.access_secret

# method to get a user's last 200 tweets
def get_tweets(username, number_of_tweets = 200):
    # http://tweepy.readthedocs.org/en/v3.1.0/getting_started.html#api
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # set count to however many tweets you want; twitter only allows 200 at once
    number_of_tweets = 200

    # get tweets
    tweets = api.user_timeline(screen_name=username, count=number_of_tweets)

    # create array of tweet information: username, tweet id, date/time, text
    tweets_for_csv = [[username, tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in tweets]

    # write to a new csv file from the array of tweets
    print("writing to unsorted/{0}_tweets.csv".format(username))
    with open("unsorted/{0}_tweets.csv".format(username), 'w+') as fh:
        writer = csv.writer(fh, delimiter='|')
        writer.writerows(tweets_for_csv)


# if we're running this as a script
if __name__ == '__main__':

    # get tweets for username passed at command line
    if len(sys.argv) == 2:
        get_tweets(sys.argv[1])
    else:
        print("Error: enter one username")

    # alternative method: loop through multiple users
    #  users = ['user1','user2']

    #  for user in users:
    #      get_tweets(user)
