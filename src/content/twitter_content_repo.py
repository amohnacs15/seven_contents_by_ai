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

def post_tweet():
    tweepy_api = initialize_tweepy()

    earliest_scheduled_datetime_str = firebase_storage_instance.get_earliest_scheduled_datetime(PostingPlatform.TWITTER)
    if (earliest_scheduled_datetime_str == ''): return 'no posts scheduled'
    print(f'TWITTER earliest posted time: {earliest_scheduled_datetime_str}')
    
    ready_to_post = time_utils.is_current_posting_time_within_window(earliest_scheduled_datetime_str)
    if (ready_to_post):
    # if (True):
        post_params_json = firebase_storage_instance.get_specific_post(
            PostingPlatform.TWITTER, 
            earliest_scheduled_datetime_str
        )
        try:
            post_params = json.loads(post_params_json)
            print(f'TWITTER post params return {post_params}')
        except:
            print('error parsing json')
            print(f'TWTITTER {post_params_json}')
            return 'error parsing json'  
            
        tweet = post_params['tweet']

        try:
            value = tweepy_api.update_status(status = tweet)  
            firebase_storage_instance.delete_post(
                PostingPlatform.TWITTER, 
                earliest_scheduled_datetime_str
            )
            return value
        except Exception as e:
            return e

def schedule_tweet( tweet, image_query ):
    if (tweet != ''):
        payload = dict()
        payload['tweet'] = tweet
        firebase_storage_instance.upload_scheduled_post(
            PostingPlatform.TWITTER, 
            payload
        )
    return tweet  