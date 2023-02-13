import datetime
import storage.firebase_storage as firebase_storage
from datetime import datetime, timedelta
import text_posts.shopify_blogger as shopify_blogger
import text_posts.tweeter as tweeter
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import text_posts.shopify_blogger as shopify_blogger
import meta_graph_api.meta_post_content as meta_poster

# Initializations
shopify = shopify_blogger.initialize_shopify()
firestore_app = firebase_admin.initialize_app()
db = firestore.client()

current_time = datetime.now()

'''
    Allow for a threshold of a minute in each direction of the scheduled time to allow and honest
    check of whether or not we are running this at the time of a scheduled post.

    Params:
        datetime scheduled_time:  the remotely stored value of when we have calculated our next posting should be
        datetime current_time: the time we have started the run of this app

    Returns:
        boolean: are we running this close enough to the scheduled date
'''
def is_current_posting_time_within_window( scheduled_time ):
    lower_bound = scheduled_time - timedelta(minutes=1)
    upper_bound = scheduled_time + timedelta(minutes=1)

    if lower_bound < current_time < upper_bound:
        True
    else:
        False

def post_facebook():
    platform = firebase_storage.PostingPlatform.FACEBOOK
    last_posted_time_iso = firebase_storage.get_last_posted_datetime(platform)
    ready_to_post = is_current_posting_time_within_window(last_posted_time_iso)
    if (ready_to_post):
        post_json = firebase_storage.get_specific_post(platform, last_posted_time_iso)
        # this needs to be a universal call and dependent on the model that is returned. 
        # It will be either image or video type
        meta_poster.post_fb_image_post()

def post_youtube( ):
    last_posted_time_iso = firebase_storage.get_last_posted_datetime( firebase_storage.PostingPlatform.FACEBOOK )

def post_instagram( ):
    last_posted_time_iso = firebase_storage.get_last_posted_datetime( firebase_storage.PostingPlatform.FACEBOOK )

def post_twitter( ):
    last_posted_time_iso = firebase_storage.get_last_posted_datetime( firebase_storage.PostingPlatform.FACEBOOK )

def post_shopify( ):
    last_posted_time_iso = firebase_storage.get_last_posted_datetime( firebase_storage.PostingPlatform.FACEBOOK )


if __name__ == '__main__':
    post_facebook()
    post_youtube()
    post_instagram()
    post_shopify()
    post_twitter()


