import sys
import os
sys.path.append("../src")

import meta_graph_api.meta_tokens as meta_tokens
from domain.endpoint_definitions import make_api_call
import media.image_creator as image_creator
import appsecrets as appsecrets
import utility.time_utils as time_utils
from storage.firebase_storage import firebase_storage_instance, PostingPlatform
import json
import domain.url_shortener as url_shortener
import ai.gpt as gpt

def make_fb_feed_call_with_token( post_json_object ):
    params = meta_tokens.fetch_fb_page_access_token()
    post_json_object['access_token'] = params['page_access_token']
    print(f'FACEBOOK {post_json_object}')

    url = params['endpoint_base'] + appsecrets.FACEBOOK_GRAPH_API_PAGE_ID + '/feed'
    result = make_api_call( url=url, endpointJson=post_json_object, type='POST')
    print(result['json_data_pretty'] )
    return result

def make_fb_photos_call_with_token( post_json_object ):
    params = meta_tokens.fetch_fb_page_access_token()
    post_json_object['access_token'] = params['page_access_token']
    print(f'FACEBOOK {post_json_object}')

    url = params['endpoint_base'] + appsecrets.FACEBOOK_GRAPH_API_PAGE_ID + '/photos'
    result = make_api_call( url=url, endpointJson=post_json_object, type='POST')
    print(result['json_data_pretty'] )
    return result

def post_scheduled_fb_post( scheduled_datetime_str ):
    post_json = firebase_storage_instance.get_specific_post(
        PostingPlatform.FACEBOOK, 
        scheduled_datetime_str
    )
    try:
        post_json_object = json.loads(post_json)
    except:
        print(F'FACEBOOK {post_json}')
        return 'FACEBOOK error parsing json'
        
    return make_fb_photos_call_with_token(post_json_object)

'''
Method called from main class that creates our endpoint request and makes the API call.
Also, prints status of uploading the payload.

@returns: nothing
'''
def post_fb_image():
    return firebase_storage_instance.upload_if_ready(
        PostingPlatform.FACEBOOK,
        post_scheduled_fb_post
    )

def schedule_fb_post( caption, image_query ):
    image_url = image_creator.get_unsplash_image_url(image_query, PostingPlatform.FACEBOOK)
    payload = {
        'url': image_url,
        'message': caption, 
        'published' : True
    }
    result = firebase_storage_instance.upload_scheduled_post(
        PostingPlatform.FACEBOOK, 
        payload
    )
    print('FACEBOOK upload scheduled post ressult' + str(result))
    return result
    
def post_blog_promo( blog_title, ref_url ):
    short_url = url_shortener.shorten_tracking_url(
        url_destination=ref_url,
        slashtag='',
        platform=PostingPlatform.FACEBOOK,
        campaign_medium='blog-reference',
        campaign_name=blog_title
    )
    message=gpt.link_prompt_to_string(
        prompt_source_file=os.path.join("src", "input_prompts", "facebook_blog_ref.txt"),
        feedin_title=blog_title,
        feedin_link=short_url
    )
    payload = {
        'link': short_url,
        'message': message, 
        'published' : True
    }
    make_fb_feed_call_with_token(payload)  