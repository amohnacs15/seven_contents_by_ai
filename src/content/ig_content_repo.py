import sys
import os
sys.path.append("../src")

import time
import meta_graph_api.meta_tokens as meta_tokens
from domain.endpoint_definitions import make_api_call
import media.image_creator as image_creator
from storage.firebase_storage import firebase_storage_instance, PostingPlatform
import json
import ai.gpt as gpt
import domain.url_shortener as url_shortener

def create_ig_media_object( params, with_token ):
    """ Create media object

        Args:
            params: dictionary of params
        
        API Endpoint:
            https://graph.facebook.com/v5.0/{ig-user-id}/media?image_url={image-url}&caption={caption}&access_token={access-token}
            https://graph.facebook.com/v5.0/{ig-user-id}/media?video_url={video-url}&caption={caption}&access_token={access-token}

        Returns:
            object: data from the endpoint

    """

    endpointParams = dict() # parameter to send to the endpoint
    endpointParams['caption'] = params['caption']  # caption for the post
    if with_token:
        endpointParams['access_token'] = params['access_token']
    endpointParams['published'] = True

    if 'IMAGE' == params['media_type'] : # posting image
        endpointParams['image_url'] = params['media_url']  # url to the asset
    else : # posting video
        endpointParams['media_type'] = params['media_type']  # specify media type
        endpointParams['video_url'] = params['media_url']  # url to the asset
    
    return endpointParams

def schedule_ig_video_post( caption, media_url ):
    
    params = meta_tokens.fetch_ig_access_token() 

    params['media_type'] = 'VIDEO' 
    params['media_url'] = media_url 
    params['caption'] = caption

    remote_media_obj = create_ig_media_object( params, False )
    firebase_storage_instance.upload_scheduled_post(PostingPlatform.INSTAGRAM, remote_media_obj)

def get_ig_media_object_status( mediaObjectId, params ):
    """ Check the status of a media object

        Args:
            mediaObjectId: id of the media object
            params: dictionary of params
        
        API Endpoint:
            https://graph.facebook.com/v5.0/{ig-container-id}?fields=status_code

        Returns:
            object: data from the endpoint
    """
    url = params['endpoint_base'] + '/' + mediaObjectId # endpoint url

    endpointParams = dict() # parameter to send to the endpoint
    endpointParams['fields'] = 'status_code' # fields to get back
    endpointParams['access_token'] = params['access_token'] # access token

    return make_api_call( url=url, params=endpointParams, type='GET' ) # make the api call

def make_ig_api_call_with_token( post_json_object ):        
    post_params = meta_tokens.fetch_ig_access_token() 
    post_params['caption'] = post_json_object['caption']
    post_params['image_url'] = post_json_object['image_url']
    post_params['published'] = post_json_object['published']

    url = post_params['endpoint_base'] + post_params['instagram_account_id'] + '/media'

    result = make_api_call( url=url, json=post_params, type='POST')
    print(result['json_data_pretty'])

def post_scheduled_ig_post( schedule_datetime_str ):
    post_params_json = firebase_storage_instance.get_specific_post(
        PostingPlatform.INSTAGRAM, 
        schedule_datetime_str
    )
    try:
        post_params_json = json.loads(post_params_json)
        print(f'INSTAGRAM {post_params_json}')
    except:
        print('INSTAGRAM error parsing json')
        print(f'INSTAGRAM {post_params_json}')
        return 'Error parsing json'    
    return make_ig_api_call_with_token(post_params_json)

def publish_ig_media( mediaObjectId, params ) :
    """ Publish content

        Args:
            mediaObjectId: id of the media object
            params: dictionary of params
        
        API Endpoint:
            https://graph.facebook.com/v5.0/{ig-user-id}/media_publish?creation_id={creation-id}&access_token={access-token}

        Returns:
            object: data from the endpoint
    """
    url = params['endpoint_base'] + params['instagram_account_id'] + '/media_publish' # endpoint url

    endpointParams = dict() # parameter to send to the endpoint
    endpointParams['creation_id'] = mediaObjectId # fields to get back
    endpointParams['access_token'] = params['access_token'] # access token

    return make_api_call( url=url, params=endpointParams, type='POST' ) # make the api call

def post_ig_media_post():
    return firebase_storage_instance.upload_if_ready(
        PostingPlatform.INSTAGRAM,
        post_scheduled_ig_post
    )

def schedule_ig_image_post( caption, image_query ):
    '''Method called from main class that creates our endpoint request and makes the API call.

    @returns: nothing
    '''
    params = meta_tokens.fetch_ig_access_token() 
    params['media_type'] = 'IMAGE' 
        
    params['media_url'] = image_creator.get_unsplash_image_url(image_query, PostingPlatform.INSTAGRAM) 
    params['caption'] = caption
        
    remote_media_obj = create_ig_media_object( params, False ) 
    firebase_storage_instance.upload_scheduled_post(PostingPlatform.INSTAGRAM, remote_media_obj)


def pretty_publish_ig_media( imageMediaObjectResponse, params, publish_func ):	
    print(f'\nimageMediaObjectResponse\n')
    print(imageMediaObjectResponse)
    
    imageMediaObjectId = imageMediaObjectResponse['json_data']['id'] # id of the media object that was created
    imageMediaStatusCode = 'IN_PROGRESS'

    print( "\n---- IMAGE MEDIA OBJECT -----\n" ) # title
    print( "\tID:" ) # label
    print( "\t" + imageMediaObjectId ) # id of the object

    while imageMediaStatusCode != 'FINISHED' : # keep checking until the object status is finished
        imageMediaObjectStatusResponse = get_ig_media_object_status( imageMediaObjectId, params ) # check the status on the object
        imageMediaStatusCode = imageMediaObjectStatusResponse['json_data']['status_code'] # update status code

        print( "\n---- IMAGE MEDIA OBJECT STATUS -----\n" ) # display status response
        print( "\tStatus Code:" ) # label
        print( "\t" + imageMediaStatusCode ) # status code of the object

        time.sleep( 5 ) # wait 5 seconds if the media object is still being processed

    publishImageResponse = publish_func( imageMediaObjectId, params ) # publish the post to instagram

    print( "\n---- PUBLISHED IMAGE RESPONSE -----\n" ) # title
    print( "\tResponse:" ) # label
    print( publishImageResponse['json_data_pretty'] ) # json response from ig api
    return imageMediaObjectResponse['json_data']

def get_content_publishing_limit( params ) :
    """ Get the api limit for the user

        Args:
            params: dictionary of params
        
        API Endpoint:
            https://graph.facebook.com/v5.0/{ig-user-id}/content_publishing_limit?fields=config,quota_usage

        Returns:
            object: data from the endpoint
    """
    url = params['endpoint_base'] + params['instagram_account_id'] + '/content_publishing_limit' # endpoint url

    endpointParams = dict() # parameter to send to the endpoint
    endpointParams['fields'] = 'config,quota_usage' # fields to get back
    endpointParams['access_token'] = params['access_token'] # access token

    return make_api_call( url=url, params=endpointParams, type='GET' ) # make the api call

# does not work
def post_blog_promo ( blog_title, ref_url, image_url ):
    short_url = url_shortener.shorten_tracking_url(
        url_destination=ref_url,
        slashtag='',
        platform=PostingPlatform.INSTAGRAM,
        campaign_medium='blog-reference',
        campaign_name=blog_title
    )
    caption=gpt.link_prompt_to_string(
        prompt_source_file=os.path.join("src", "input_prompts", "facebook_blog_ref.txt"),
        feedin_title=blog_title,
        feedin_link=short_url
    )
    if (image_url == ''):
        image_url = image_creator.get_unsplash_image_url(PostingPlatform.INSTAGRAM, 'old man')
    payload = {
        'media_type': 'IMAGE',
        'image_url': image_url,
        'caption': caption, 
        'published' : True
    }
    make_ig_api_call_with_token(payload)  