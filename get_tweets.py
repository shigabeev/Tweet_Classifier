
import sys
import csv
import os
# tweepy.org
import tweepy
try:
    import config
except ImportError:
    print("Oops, looks like you haven't specified your Twitter credentials in config.py.")
    print("If you're already registered in dev.Twitter, modify lines 14-17 in get_tweets.py. Or create config.py with following lines:")
    print("consumer_key = \nconsumer_secret = \naccess_key = \naccess_secret =")
    sys.exit()
# Get your Twitter API credentials and enter them here
consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_key = config.access_key
access_secret = config.access_secret

# method to get a user's last 200 tweets
def get_tweets(username, number_of_tweets = 200, folder = "unsorted"):
    # http://tweepy.readthedocs.org/en/v3.1.0/getting_started.html#api
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # set count to however many tweets you want; twitter only allows 200 at once
    number_of_tweets = number_of_tweets

    # get tweets
    tweets = api.user_timeline(screen_name=username, count=number_of_tweets)

    # create array of tweet information: username, tweet id, date/time, text.encode("utf-8")
    tweets_for_csv = [[username, tweet.id_str, tweet.created_at, tweet.text] for tweet in tweets]

    # write to a new csv file from the array of tweets
    # print("writing to %s/{0}_tweets.csv".format(username) % folder)
    try:
        os.remove("%s/{0}_tweets.csv".format(username) % folder)
    except OSError:
        pass
    with open("%s/{0}_tweets.csv".format(username) % folder, 'w+') as fh:
        writer = csv.writer(fh, delimiter='|')
        writer.writerows(tweets_for_csv)

def get_likes(username, number_of_tweets = 200):
    ###
    likes = tweepy.API(auth).favorites(username)
    ###

# if we're running this as a script
if __name__ == '__main__':

    # get tweets for username passed at command line
    if len(sys.argv) == 2:
        get_tweets(sys.argv[1])
    elif len(sys.argv) == 3:
        get_tweets(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4:
        get_tweets(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Error: enter one username")

    # alternative method: loop through multiple users
    #  users = ['user1','user2']

    #  for user in users:
    #      get_tweets(user)
