import sys
sys.path.append("../src")

import text_posts.shopify_content_repo as shopify_content_repo
import meta_graph_api.fb_content_repo as fb_content_repo
import meta_graph_api.ig_content_repo as ig_content_repo
import text_posts.twitter_content_repo as twitter_content_repo

# Initializations
shopify = shopify_content_repo.initialize_shopify()

def post(type, post_fun): 
    successful_post = post_fun
    print(f'{type} post processed.  Result: {successful_post}')

def post_medium( ): ''

if __name__ == '__main__':
    # post('Shopify', shopify_content_repo.post_shopify_blog_article())
    # post('Facebook', fb_content_repo.post_fb_image_post())
    # post('Instagram', ig_content_repo.post_ig_media_post())
    post('Twitter', twitter_content_repo.post_tweets())

    # post_youtube()

    # post_twitter()
    # post_medium()


