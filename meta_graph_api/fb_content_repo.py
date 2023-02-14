from datetime import datetime
import meta_graph_api.meta_tokens as meta_tokens
from meta_graph_api.meta_definition import make_api_call
import utility.utils as utils
import media.image_creator as image_creator
import appsecrets
import utility.time_utils as time_utils
from storage.firebase_storage import FirebaseStorage
from storage.firebase_storage import PostingPlatform
import json

firebase_storage_instance = FirebaseStorage()

'''
Method called from main class that creates our endpoint request and makes the API call.
Also, prints status of uploading the payload.

@returns: nothing
'''
def post_fb_image_post():
    current_time = datetime.now()
    print(f'current time :{current_time}')
    last_posted_datetime = firebase_storage_instance.get_last_posted_datetime(PostingPlatform.FACEBOOK)
    print(f'last posted time: {last_posted_datetime}')
    ready_to_post = time_utils.is_current_posting_time_within_window(
        current_time,
        last_posted_datetime
    )
    last_posted_time_iso = last_posted_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    print(last_posted_time_iso)
    # if (ready_to_post):
    if (True):
        post_json = firebase_storage_instance.get_specific_post(
            PostingPlatform.FACEBOOK, 
            last_posted_time_iso
        )
        print(post_json)
        # this needs to be a universal call and dependent on the model that is returned. 
        # It will be either image or video type
        params = meta_tokens.get_fb_page_access_token()
        post_json_object = json.loads(post_json)
        url = params['endpoint_base'] + appsecrets.FACEBOOK_GRAPH_API_PAGE_ID + '/photos'
        post_json_object['access_token'] = params['access_token']

        print(post_json_object)

        return make_api_call( url=url, endpointJson=post_json_object, type='POST' )
        # #Send the POST request
        # r = requests.post(
        # 	post_url, 
        # 	data=json_post_payload
        # )
        # print(r.text)	

def schedule_facebook_post( caption ):
    search_query = utils.get_title_subquery(caption)
    image_url = image_creator.get_unsplash_image_url(search_query)

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