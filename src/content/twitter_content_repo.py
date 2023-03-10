import sys
import os
sys.path.append("../src")

import tweepy
import appsecrets
from storage.firebase_storage import firebase_storage_instance, PostingPlatform
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

tweepy_api = initialize_tweepy()

def update_tweet_status( scheduled_datetime_str ):
    '''
        Our strict interaction with the Tweepy API

        @params:

        @returns:
            value: with success. this is the post response
            none: with error.
    '''
    post_params_json = firebase_storage_instance.get_specific_post(
        PostingPlatform.TWITTER, 
        scheduled_datetime_str
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
        return value
    except Exception as e:
        print(f'TWITTER {e}')
        return None

def post_tweet(): 
    return firebase_storage_instance.upload_if_ready(PostingPlatform.TWITTER, update_tweet_status)

def schedule_tweet( tweet, image_query ):
    if (tweet != ''):
        payload = dict()
        payload['tweet'] = tweet
        firebase_storage_instance.upload_scheduled_post(
            PostingPlatform.TWITTER, 
            payload
        )
    return tweet  