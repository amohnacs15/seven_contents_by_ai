import storage.firebase_storage as local_storage
from datetime import datetime, timedelta
import text_posts.shopify_blogger as shopify_blogger
import text_posts.tweeter as tweeter
import text_posts.shopify_blogger as shopify_blogger
import meta_graph_api.ig_content_repo as meta_poster
import meta_graph_api.fb_content_repo as fb_repo
import storage.firebase_storage as FirebaseStorage

# Initializations
shopify = shopify_blogger.initialize_shopify()

def post_facebook():
    successful_post=fb_repo.post_fb_image_post()
    print(f'post success? {successful_post}')
    
def post_youtube( ):
    ''
def post_instagram( ):
    ''

def post_twitter( ):
    ''

def post_shopify( ):
    ''

if __name__ == '__main__':
    post_facebook()
    post_youtube()
    post_instagram()
    post_shopify()
    post_twitter()


