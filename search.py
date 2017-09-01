#!/usr/bin/env python

from TwitterSearch import *
import sys
from datetime import datetime, timedelta
from dateutil import parser
from collections import Counter

file_o_tweet = sys.argv[1]
file_o_ht = sys.argv[2]
file_o_user = sys.argv[3]
file_hashtag = sys.argv[4]
f_tweet = open(file_o_tweet, "w")
f_ht = open(file_o_ht, "w")
f_user = open(file_o_user, "w")
with open(file_hashtag) as f_hash:
    hashtags = f_hash.read().splitlines()
f_hash.close()

try:
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(hashtags)
    tso.set_geocode(32.709722, -97.368056, 5, imperial_metric=True)

    # it's about time to create a TwitterSearch object with our secret tokens
    ts = TwitterSearch(
        consumer_key =  '5APe20dRCeE3HzC2OWo5LNCMK',
        consumer_secret = 'Cm8M0A2zLdDplThIIbyAkSlfL6soxBQdTZcmvKKzbLtchIhnoL',
        access_token = '2743910958-QzEA68W0x7QqnWZQTS5nfvbFEP2SCg4IPKgWMld',
        access_token_secret = 'jYfvWBfhf1eFw57jKefbzpT1BkEjSbXD7mW7Sbfh1tmU0'
     )

    # this is where the fun actually starts :)
    count = 0
    hashtag_list = []
    tweet_list = []
    user_list = []
    for tweet in ts.search_tweets_iterable(tso):
        # set the period of searching to a certain number of dates ago
        time = parser.parse(tweet["created_at"])
        timezone = time.tzinfo
        seven_days_ago = datetime.now(timezone) - timedelta(days=7)

        # if tweet is created in certain time frame:
        # 1) increment counter
        # 2) append tweet to tweet_list
        # 3) append hashtag to hashtag_list
        if time > seven_days_ago:
            count+=1
            tweet_list.append( ('%i @%s tweeted: %s\n' % ( count, tweet['user']['screen_name'], tweet['text'] ) ).encode('utf-8') )
            user_list.append("%s" % tweet['user']['screen_name'])
            for ht in tweet['entities']['hashtags']:
                hashtag_list.append(ht['text'])

    rtcounter = 0
    hashtag_counter = Counter(hashtag_list)
    for ht, count in hashtag_counter.items():
        f_ht.write("%s: %i\n" % (ht, count) )
    for item in tweet_list:
        f_tweet.write(item)
        if item.split()[0] == "RT":
            rtcounter += 1
    f_tweet.write("Total retweets: %i" % rtcounter)
    user_counter = Counter(user_list)
    for user, count in user_counter.items():
        f_user.write("%s: %i\n" % (user, count) )

    f_ht.write( "Queries done: %i. Tweets received: %i\n" % (ts.get_statistics()) )
    f_ht.write( "Time of query: %s" % ( str(datetime.now()) )) 
    f_tweet.write( "Queries done: %i. Tweets received: %i\n" % (ts.get_statistics()) )
    f_tweet.write( "Time of query: %s" % ( str(datetime.now()) )) 

except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)

f_tweet.close()
f_ht.close()
f_user.close()