import text_posts.shopify_blogger as shopify_blogger
import text_posts.tweeter as tweeter
import text_posts.shopify_blogger as shopify_blogger
import meta_graph_api.fb_content_repo as fb_content_repo
import meta_graph_api.ig_content_repo as ig_content_repo

# Initializations
shopify = shopify_blogger.initialize_shopify()

def post_facebook():
    successful_post=fb_content_repo.post_fb_image_post()
    print(f'post success?\n\n{successful_post}')
    
def post_instagram():
    successful_post = ig_content_repo.post_ig_image_post()
    print(f'post successful?\n\n {successful_post}')

def post_youtube( ):
    ''

def post_twitter( ):
    ''

def post_shopify( ):
    ''

if __name__ == '__main__':
    # post_facebook()
    post_youtube()
    post_instagram()
    post_shopify()
    post_twitter()


