from datetime import datetime
import src.meta_graph_api.meta_tokens as meta_tokens
from src.meta_graph_api.meta_definition import make_api_call
import src.media.image_creator as image_creator
import appsecrets
import src.utility.time_utils as time_utils
from src.storage.firebase_storage import FirebaseStorage
from src.storage.firebase_storage import PostingPlatform
import json

firebase_storage_instance = FirebaseStorage()

'''
Method called from main class that creates our endpoint request and makes the API call.
Also, prints status of uploading the payload.

@returns: nothing
'''
def post_fb_image_post():
    current_time = datetime.now()
    print(f'FB current time :{current_time}')
    
    last_posted_datetime = firebase_storage_instance.get_last_posted_datetime(PostingPlatform.FACEBOOK)
    print(f' FB last posted time: {last_posted_datetime}')
    
    ready_to_post = time_utils.is_current_posting_time_within_window(
        current_time,
        last_posted_datetime
    )
    
    last_posted_time_iso = last_posted_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    print(f'last posted time iso {last_posted_time_iso}')
    
    if (ready_to_post):
        post_json = firebase_storage_instance.get_specific_post(
            PostingPlatform.FACEBOOK, 
            last_posted_time_iso
        )
        post_json_object = json.loads(post_json)
        
        params = meta_tokens.get_fb_page_access_token()
        post_json_object['access_token'] = params['page_access_token']
        print(post_json_object)

        url = params['endpoint_base'] + appsecrets.FACEBOOK_GRAPH_API_PAGE_ID + '/photos'
        return make_api_call( url=url, endpointJson=post_json_object, type='POST' )

def schedule_facebook_post( caption, image_query ):
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