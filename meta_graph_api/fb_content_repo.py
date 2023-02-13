import time
import meta_graph_api.meta_tokens as meta_tokens
from meta_graph_api.meta_definition import make_api_call
import utility.utils as utils
import media.image_creator as image_creator
from storage.firebase_storage import PostingPlatform
import appsecrets
import utility.time_utils as time_utils
import storage.firebase_storage as FirebaseStorage
from storage.firebase_storage import PostingPlatform

firebase_storage = FirebaseStorage()

'''
Method called from main class that creates our endpoint request and makes the API call.
Also, prints status of uploading the payload.

@returns: nothing
'''
def post_fb_image_post( json_post_payload ):

    last_posted_time_iso = firebase_storage.get_last_posted_datetime(PostingPlatform.FACEBOOK)
    ready_to_post = time_utils.is_current_posting_time_within_window(last_posted_time_iso)
    if (ready_to_post):
        post_json = firebase_storage.get_specific_post(PostingPlatform.FACEBOOK, last_posted_time_iso)
        # this needs to be a universal call and dependent on the model that is returned. 
        # It will be either image or video type
        params = meta_tokens.get_fb_page_access_token()
        url = params['endpoint_base'] + appsecrets.FACEBOOK_GRAPH_API_PAGE_ID + '/photos'
        post_json['access_token'] = params['access_token']

        return make_api_call( url, post_json, 'POST' )
        # #Send the POST request
        # r = requests.post(
        # 	post_url, 
        # 	data=json_post_payload
        # )
        # print(r.text)	

def schedule_facebook_post( self, caption ):
    search_query = utils.get_title_subquery(caption)
    image_url = image_creator.get_unsplash_image_url(search_query)

    payload = {
        'url': image_url,
        'message': caption, 
        'published' : True
    }

    result = firebase_storage.upload_scheduled_post(
        PostingPlatform.FACEBOOK, 
        payload
    )
    return result