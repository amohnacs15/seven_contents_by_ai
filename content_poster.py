import datetime
import storage.firebase_storage as firebase_storage
from datetime import datetime, timedelta
import text_posts.shopify_blogger as shopify_blogger
import text_posts.tweeter as tweeter
import text_posts.shopify_blogger as shopify_blogger
import meta_graph_api.ig_content_repo as meta_poster
import meta_graph_api.fb_content_repo as fb_repo
import storage.firebase_storage as FirebaseStorage
from storage.firebase_storage import PostingPlatform

# Initializations
shopify = shopify_blogger.initialize_shopify()
firebase_storage = FirebaseStorage()

current_time = datetime.now()

def post_facebook():
    platform = firebase_storage.PostingPlatform.FACEBOOK
    

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


