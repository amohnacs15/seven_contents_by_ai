import sys
import os
sys.path.append("../src")

import tweepy
import appsecrets
from storage.firebase_storage import firebase_storage_instance, PostingPlatform
import json
import ai.gpt as gpt
import domain.url_shortener as url_shortener

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

def update_tweet( text ):
    try:
        value = tweepy_api.update_status(status = text)  
        return value
    except Exception as e:
        print(f'TWITTER {e}')
        return None

def post_blog_promo_tweet( blog_title, ref_url ):
    short_url = url_shortener.shorten_tracking_url(
        url_destination=ref_url,
        slashtag='',
        platform=PostingPlatform.TWITTER,
        campaign_medium='blog-reference',
        campaign_name=blog_title
    )
    text=gpt.link_prompt_to_string(
        prompt_source_file=os.path.join("src", "input_prompts", "twitter_blog_ref.txt"),
        feedin_title=blog_title,
        feedin_link=short_url
    )
    update_tweet(text)

def post_scheduled_tweet( scheduled_datetime_str ):
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
    return update_tweet(tweet)

def post_tweet(): 
    return firebase_storage_instance.upload_if_ready(
        PostingPlatform.TWITTER, 
        post_scheduled_tweet
    )

def schedule_tweet( tweet, image_query ):
    if (tweet != ''):
        payload = dict()
        payload['tweet'] = tweet
        firebase_storage_instance.upload_scheduled_post(
            PostingPlatform.TWITTER, 
            payload
        )
    return tweet  