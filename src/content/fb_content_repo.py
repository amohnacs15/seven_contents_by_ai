import sys
sys.path.append("../src")

import meta_graph_api.meta_tokens as meta_tokens
from domain.endpoint_definitions import make_api_call
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
    earliest_scheduled_datetime_str = firebase_storage_instance.get_earliest_scheduled_datetime(PostingPlatform.FACEBOOK)
    if (earliest_scheduled_datetime_str == ''): return 'no posts scheduled'
    print(f'FACEBOOK earliest scheduled time: {earliest_scheduled_datetime_str}')
    
    ready_to_post = time_utils.is_current_posting_time_within_window(earliest_scheduled_datetime_str)
    if (ready_to_post):
    # if (True):
        post_json = firebase_storage_instance.get_specific_post(
            PostingPlatform.FACEBOOK, 
            earliest_scheduled_datetime_str
        )
        try:
            post_json_object = json.loads(post_json)
        except:
            print(F'FACEBOOK {post_json}')
            return 'FACEBOOK error parsing json'
        
        params = meta_tokens.fetch_fb_page_access_token()
        post_json_object['access_token'] = params['page_access_token']
        print(f'FACEBOOK {post_json_object}')

        url = params['endpoint_base'] + appsecrets.FACEBOOK_GRAPH_API_PAGE_ID + '/photos'
        result = make_api_call( url=url, endpointJson=post_json_object, type='POST')
        print(result['json_data_pretty'] )
        firebase_storage_instance.delete_post(
            PostingPlatform.FACEBOOK, 
            earliest_scheduled_datetime_str
        )
        return result

def schedule_fb_post( caption, image_query ):
    image_url = image_creator.get_unsplash_image_url(image_query)
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
    