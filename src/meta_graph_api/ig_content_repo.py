import sys
sys.path.append("../src")

import time
import meta_graph_api.meta_tokens as meta_tokens
from meta_graph_api.meta_definition import make_api_call
import media.image_creator as image_creator
from storage.firebase_storage import FirebaseStorage, PostingPlatform
import json
import utility.time_utils as time_utils

firebase_storage_instance = FirebaseStorage()

""" Create media object

    Args:
        params: dictionary of params
    
    API Endpoint:
        https://graph.facebook.com/v5.0/{ig-user-id}/media?image_url={image-url}&caption={caption}&access_token={access-token}
        https://graph.facebook.com/v5.0/{ig-user-id}/media?video_url={video-url}&caption={caption}&access_token={access-token}

    Returns:
        object: data from the endpoint

"""
def create_ig_media_object( params ) :

    endpointParams = dict() # parameter to send to the endpoint
    endpointParams['caption'] = params['caption']  # caption for the post
    endpointParams['access_token'] = params['access_token'] # access token
    endpointParams['published'] = True

    if 'IMAGE' == params['media_type'] : # posting image
        endpointParams['image_url'] = params['media_url']  # url to the asset
    else : # posting video
        endpointParams['media_type'] = params['media_type']  # specify media type
        endpointParams['video_url'] = params['media_url']  # url to the asset
    
    return endpointParams

'''
Method called from main class that creates our endpoint request and makes the API call.
Also, prints status of uploading the payload.

@returns: nothing
'''
def schedule_ig_video_post( caption, media_url ):
    params = meta_tokens.get_ig_access_creds() 

    params['media_type'] = 'VIDEO' 
    params['media_url'] = media_url 
    params['caption'] = caption

    remote_media_obj = create_ig_media_object( params )
    firebase_storage_instance.upload_scheduled_post(PostingPlatform.INSTAGRAM, remote_media_obj)

    
""" Check the status of a media object

    Args:
        mediaObjectId: id of the media object
        params: dictionary of params
    
    API Endpoint:
        https://graph.facebook.com/v5.0/{ig-container-id}?fields=status_code

    Returns:
        object: data from the endpoint

"""
def get_ig_media_object_status( mediaObjectId, params ) :
    url = params['endpoint_base'] + '/' + mediaObjectId # endpoint url

    endpointParams = dict() # parameter to send to the endpoint
    endpointParams['fields'] = 'status_code' # fields to get back
    endpointParams['access_token'] = params['access_token'] # access token

    return make_api_call( url=url, endpointParams=endpointParams, type='GET' ) # make the api call

""" Publish content

    Args:
        mediaObjectId: id of the media object
        params: dictionary of params
    
    API Endpoint:
        https://graph.facebook.com/v5.0/{ig-user-id}/media_publish?creation_id={creation-id}&access_token={access-token}

    Returns:
        object: data from the endpoint

"""
def publish_ig_media( mediaObjectId, params ) :
    url = params['endpoint_base'] + params['instagram_account_id'] + '/media_publish' # endpoint url

    endpointParams = dict() # parameter to send to the endpoint
    endpointParams['creation_id'] = mediaObjectId # fields to get back
    endpointParams['access_token'] = params['access_token'] # access token

    return make_api_call( url=url, endpointParams=endpointParams, type='POST' ) # make the api call

""" Pulls last posted time form FB and posts ot IG an image

    Args:
        mediaObjectId: id of the media object
        params: dictionary of params
    
    API Endpoint:
        https://graph.facebook.com/v5.0/{ig-user-id}/media_publish?creation_id={creation-id}&access_token={access-token}

    Returns:
        object: data from the endpoint

"""
def post_ig_media_post():
    last_posted_datetime = firebase_storage_instance.get_last_posted_datetime(PostingPlatform.INSTAGRAM)
    print(f' FB last posted time: {last_posted_datetime}')
    
    ready_to_post = time_utils.is_current_posting_time_within_window(last_posted_datetime)

    if (ready_to_post):
        last_posted_time_iso = last_posted_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        print(f'IG last posted time iso {last_posted_time_iso}')

        post_params_json = firebase_storage_instance.get_specific_post(
            PostingPlatform.INSTAGRAM, 
            last_posted_time_iso
        )
        
        post_params_json = json.loads(post_params_json)
        post_parms = dict()
        post_parms['access_token'] = post_params_json['access_token']
        post_parms['caption'] = post_params_json['caption']
        post_parms['image_url'] = post_params_json['image_url']
        post_parms['published'] = post_params_json['published']

        params = meta_tokens.get_ig_access_creds() 
        url = params['endpoint_base'] + params['instagram_account_id'] + '/media'

        remote_media_obj = make_api_call( url=url, endpointJson=post_params_json, type='POST')
        return pretty_publish_ig_media(remote_media_obj, params, publish_ig_media) 

'''
Method called from main class that creates our endpoint request and makes the API call.
Also, prints status of uploading the payload.

@returns: nothing
'''
def schedule_ig_image_post( caption, image_query ):
    params = meta_tokens.get_ig_access_creds() 
    params['media_type'] = 'IMAGE' 
    
    params['media_url'] = image_creator.get_unsplash_image_url(image_query) 
    params['caption'] = caption
    
    remote_media_obj = create_ig_media_object( params ) 
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

""" Get the api limit for the user

    Args:
        params: dictionary of params
    
    API Endpoint:
        https://graph.facebook.com/v5.0/{ig-user-id}/content_publishing_limit?fields=config,quota_usage

    Returns:
        object: data from the endpoint

"""
def get_content_publishing_limit( params ) :
    url = params['endpoint_base'] + params['instagram_account_id'] + '/content_publishing_limit' # endpoint url

    endpointParams = dict() # parameter to send to the endpoint
    endpointParams['fields'] = 'config,quota_usage' # fields to get back
    endpointParams['access_token'] = params['access_token'] # access token

    return make_api_call( url=url, endpointParams=endpointParams, type='GET' ) # make the api call

