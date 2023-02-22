import sys
sys.path.append("../src")

from datetime import datetime
import meta_graph_api.meta_tokens as meta_tokens
from meta_graph_api.meta_definition import make_api_call
import media.image_creator as image_creator
import appsecrets as appsecrets
import utility.time_utils as time_utils
from storage.firebase_storage import firebase_storage_instance, PostingPlatform
import json

'''
Method called from main class that creates our endpoint request and makes the API call.
Also, prints status of uploading the payload.

@returns: nothing
'''
def post_fb_image():
    earliest_scheduled_datetime = firebase_storage_instance.get_earliest_scheduled_datetime(PostingPlatform.FACEBOOK)
    print(f' FB last posted time: {earliest_scheduled_datetime}')
    
    ready_to_post = time_utils.is_current_posting_time_within_window(earliest_scheduled_datetime)
    
    earliest_scheduled_iso = earliest_scheduled_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    print(f'last posted time iso {earliest_scheduled_iso}')
    
    # if (ready_to_post):
    if (True):
        post_json = firebase_storage_instance.get_specific_post(
            PostingPlatform.FACEBOOK, 
            earliest_scheduled_iso
        )
        post_json_object = json.loads(post_json)
        
        params = meta_tokens.get_fb_page_access_token()
        post_json_object['access_token'] = params['page_access_token']
        print(post_json_object)

        url = params['endpoint_base'] + appsecrets.FACEBOOK_GRAPH_API_PAGE_ID + '/photos'
        result =  make_api_call( url=url, endpointJson=post_json_object, type='POST' )
        firebase_storage_instance.delete_post(
            PostingPlatform.FACEBOOK, 
            earliest_scheduled_iso
         )
        return result

def schedule_fb_post( caption, image_query ):
    image_url = image_creator.get_unsplash_image_url(image_query)

    payload = {
        'url': image_url,
        'message': caption, 
        'published' : True
    }

    print('posting payload')
    print(payload)

    result = firebase_storage_instance.upload_scheduled_post(
        PostingPlatform.FACEBOOK, 
        payload
    )

    print('upload scheduled post ressult')
    print(str(result))
    return result