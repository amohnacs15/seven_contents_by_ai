import sys
sys.path.append("../src")

import time
import meta_graph_api.meta_tokens as meta_tokens
from meta_graph_api.meta_definition import make_api_call
import media.image_creator as image_creator
from storage.firebase_storage import firebase_storage_instance, PostingPlatform
import json
import utility.time_utils as time_utils

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

    return make_api_call( url=url, endpointParams=endpointParams, type='GET' ) # make the api call

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

    return make_api_call( url=url, endpointParams=endpointParams, type='POST' ) # make the api call

def post_ig_media_post():
    """ Pulls last posted time form FB and posts ot IG an image

        Args:
            mediaObjectId: id of the media object
            params: dictionary of params
        
        API Endpoint:
            https://graph.facebook.com/v5.0/{ig-user-id}/media_publish?creation_id={creation-id}&access_token={access-token}

        Returns:
            object: data from the endpoint
    """                                 
    earliest_scheduled_datetime_str = firebase_storage_instance.get_earliest_scheduled_datetime(PostingPlatform.INSTAGRAM)
    if (earliest_scheduled_datetime_str == ''): return 'no posts scheduled'
    print(f'INSTAGRAM earliest time: {earliest_scheduled_datetime_str}')
    
    ready_to_post = time_utils.is_current_posting_time_within_window(earliest_scheduled_datetime_str)
    if (ready_to_post):
    # if (True):
        post_params_json = firebase_storage_instance.get_specific_post(
            PostingPlatform.INSTAGRAM, 
            earliest_scheduled_datetime_str
        )
        
        try:
            post_params_json = json.loads(post_params_json)
            print(f'INSTAGRAM {post_params_json}')
        except:
            print('INSTAGRAM error parsing json')
            print(f'INSTAGRAM {post_params_json}')
            return 'Error parsing json'    
        
        post_params = meta_tokens.fetch_ig_access_token() 
        post_params['caption'] = post_params_json['caption']
        post_params['image_url'] = post_params_json['image_url']
        post_params['published'] = post_params_json['published']

        url = post_params['endpoint_base'] + post_params['instagram_account_id'] + '/media'

        remote_media_obj = make_api_call( url=url, endpointJson=post_params, type='POST')
        firebase_storage_instance.delete_post(
            PostingPlatform.INSTAGRAM, 
            earliest_scheduled_datetime_str
        )
        return pretty_publish_ig_media(remote_media_obj, post_params, publish_ig_media) 

def schedule_ig_image_post( caption, image_query ):
    '''Method called from main class that creates our endpoint request and makes the API call.

    @returns: nothing
    '''
    params = meta_tokens.fetch_ig_access_token() 
    params['media_type'] = 'IMAGE' 
        
    params['media_url'] = image_creator.get_unsplash_image_url(image_query) 
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

    return make_api_call( url=url, endpointParams=endpointParams, type='GET' ) # make the api call

