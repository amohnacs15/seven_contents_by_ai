import sys
sys.path.append("../src")

import shopify
import appsecrets as appsecrets
import media.image_creator as image_creator
import utility.text_utils as text_utils
from storage.firebase_storage import firebase_storage_instance, PostingPlatform
import utility.time_utils as time_utils
import json

def initialize_shopify():
    # Configure store details
    shop_url = 'osaka-cosplay.myshopify.com'
    admin_api_key = appsecrets.SHOPIFY_ADMIN_API_TOKEN
    api_version = '2023-01'
    # Create and activate a new session
    session = shopify.Session(shop_url, api_version, admin_api_key)
    shopify.ShopifyResource.activate_session(session)
    print('Shopify initialized successfully')

def get_image_asset_url(image_query):
    return image_creator.get_unsplash_image_url(image_query)

    themes = shopify.Theme.find()
    for theme in themes:
        print(f'theme {theme.name} has ID: {theme.id}')
        # how do we make recognizing the most recent theme dynamic?
        if (theme.name == 'Caregiver Modern v3'):
            print(f'got the right theme {theme.name} has ID: {theme.id}')
            current_theme_id = theme.id

            asset = shopify.Asset({"theme_id": current_theme_id})
            asset.key = 'grid_1'
            asset.value = {
                'image': {
                    'src': unsplash_url
                }
            }
            result_asset = asset.save()
            print(result_asset)
            return result_asset.public_url   

def post_shopify_blog_article(): 
    last_posted_datetime = firebase_storage_instance.get_earliest_scheduled_datetime(PostingPlatform.SHOPIFY)
    print(f'SH last posted time: {last_posted_datetime}')
    
    ready_to_post = time_utils.is_current_posting_time_within_window(last_posted_datetime)

    if (ready_to_post):
    # if (True):
        last_posted_time_iso = last_posted_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        print(f'SH last posted time iso {last_posted_time_iso}')

        post_params_json = firebase_storage_instance.get_specific_post(
            PostingPlatform.SHOPIFY, 
            last_posted_time_iso
        )
        post_params = json.loads(post_params_json)

        new_blog = shopify.Blog.create({"title": post_params['title']})

        if (new_blog.save()):
            new_article = shopify.Article()

            new_article.blog_id = new_blog.id
            new_article.title = post_params['title']
            new_article.author = post_params['author']
            new_article.body_html = post_params['body_html']

            new_article.image = post_params['image']['src']

            new_article.published = post_params['published']
            result = new_article.save()
            print(f'Shopify blog upload successful {result}')
            return result
        else:
            print (new_blog.errors.full_messages())
            return result
    

def schedule_shopify_blog_article(blog, image_query):
    bloglines = blog.split()
    title = text_utils.simplify_H1_header(bloglines[0])
    blog = text_utils.groom_titles(blog)

    print('begin asset processing')
    get_image_asset_url(image_query)

    payload = dict()
    payload['title'] = title
    payload['author'] = 'Caregiver Modern'
    payload['body_html'] = blog
    payload['image'] = dict()
    payload['image']['src'] = ''
    payload['published'] = 'TRUE'
    
    result = firebase_storage_instance.upload_scheduled_post(
        PostingPlatform.SHOPIFY, 
        payload
    )
    print(result)
        