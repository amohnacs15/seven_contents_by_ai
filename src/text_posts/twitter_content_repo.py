import sys
import os
sys.path.append("../src")

import tweepy
import appsecrets
from storage.firebase_storage import firebase_storage_instance, PostingPlatform
import utility.time_utils as time_utils
import json

def initialize_tweepy():
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(appsecrets.TWITTER_API_KEY, appsecrets.TWITTER_API_SECRET)
    auth.set_access_token(appsecrets.TWITTER_API_AUTH_TOKEN, appsecrets.TWITTER_API_AUTH_SECRET)

    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        print("Twitter Authentication OK")
    except:
        print("Error during Tweepy authentication") 
    return api    

def post_tweets():
    tweepy_api = initialize_tweepy()

    # get from firebase
    last_posted_datetime = firebase_storage_instance.get_last_posted_datetime(PostingPlatform.TWITTER)
    print(f'TW last posted time: {last_posted_datetime}')
    
    ready_to_post = time_utils.is_current_posting_time_within_window(last_posted_datetime)

    if (ready_to_post):
    # if (True):
        last_posted_time_iso = last_posted_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        print(f'TW last posted time iso {last_posted_time_iso}')

        post_params_json = firebase_storage_instance.get_specific_post(
            PostingPlatform.TWITTER, 
            last_posted_time_iso
        )
        post_params = json.loads(post_params_json)
        tweet = post_params['tweet']

        try:
            tweepy_api.update_status(status = tweet)  
            print("Tweet sent:" + tweet)
        except:
            print('Tweet too long or error. Skipping')  

def schedule_tweets( tweet, image_query ):
    file_path = os.path.join('src', 'outputs', 'tweetstorm_output.txt')
    
    # Using readlines()
    tweetFile = open(file_path, 'r', encoding="utf8")
    tweets = tweetFile.readlines()

    for tweet in tweets:
        payload = dict()
        payload['tweet'] = tweet
        result = firebase_storage_instance.upload_scheduled_post(
            PostingPlatform.TWITTER, 
            payload
        )
        print(result)
      