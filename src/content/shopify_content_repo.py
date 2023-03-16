import sys
import os
sys.path.append("../src")

import shopify
import appsecrets as appsecrets
import media.image_creator as image_creator
import utility.text_utils as text_utils
import utility.time_utils as time_utils
from storage.firebase_storage import firebase_storage_instance, PostingPlatform
import json
import ai.gpt as gpt3
import domain.url_shortener as url_shortener
import content.fb_content_repo as fb_content_repo
import content.ig_content_repo as ig_content_repo
import content.twitter_content_repo as twitter_content_repo

def initialize_shopify():
    # Configure store details
    shop_url = 'osaka-cosplay.myshopify.com'
    admin_api_key = appsecrets.SHOPIFY_ADMIN_API_TOKEN
    api_version = '2023-01'
    # Create and activate a new session
    session = shopify.Session(shop_url, api_version, admin_api_key)
    shopify.ShopifyResource.activate_session(session)
    print('Shopify initialized successfully')      

def post_shopify_blog_article(): 
    earliest_scheduled_datetime_str = firebase_storage_instance.get_earliest_scheduled_datetime(PostingPlatform.SHOPIFY)
    if (earliest_scheduled_datetime_str == ''): return 'no posts scheduled'
    print(f'SHOPIFY earliest scheduled time: {earliest_scheduled_datetime_str}')
    
    ready_to_post = time_utils.is_current_posting_time_within_window(earliest_scheduled_datetime_str)
    # if (ready_to_post):
    if (True):
        post_params_json = firebase_storage_instance.get_specific_post(
            PostingPlatform.SHOPIFY, 
            earliest_scheduled_datetime_str
        )
        try:
            post_params = json.loads(post_params_json)
        except:
            print('SHOPIFY error parsing json')
            print(f'SHOPIFY {post_params_json}')
            return 'error parsing json'    

        if (post_params['title'] != ''):
            shopify.DiscountCode

            list_of_blogs = shopify.Blog.find()

            for blog in list_of_blogs:
                print(f'processing blogs')
                if (blog.title == 'Caregiver Help & How-To'):

                    new_article = shopify.Article()

                    new_article.blog_id = blog.id
                    new_article.title = post_params['title']
                    new_article.author = post_params['author']
                    new_article.body_html = post_params['body_html']
                    new_article.published = post_params['published']

                    image = shopify.Image()
                    image.src = post_params['image']['src']
                    new_article.image = image

                    result = new_article.save()

                    #construct and save address of uploaded blog
                    if (result):
                        base_path = "https://www.caregivermodern.com/blogs/caregiver-help-how-to/"
                        updated_title = new_article.title.replace(' ', '-').replace('\'', '').replace(',','').replace('.', '').replace('"', '').replace(':','')
                        combined_url = base_path + updated_title
                        
                        twitter_content_repo.post_blog_promo_tweet(
                            blog_title=new_article.title,
                            ref_url=combined_url
                        )
                        fb_content_repo.post_blog_promo(
                            blog_title=new_article.title,
                            ref_url=combined_url
                        )

                    print(f'SHOPIFY blog upload successful {result}')
                    firebase_storage_instance.delete_post(
                        PostingPlatform.SHOPIFY, 
                        earliest_scheduled_datetime_str
                    )
                    return True    
    
def schedule_shopify_blog_article(blog, image_query):
    try:
        blog = text_utils.groom_titles(blog)
        parts = blog.split('\n\n', 1)
        image_src = image_creator.get_unsplash_image_url(image_query, PostingPlatform.SHOPIFY, 'landscape')

        title = text_utils.simplify_H1_header(parts[0])
        if (len(title) > 200):
            title = gpt3.prompt_to_string(
                prompt_source_file=os.path.join('src', 'input_prompts', 'youtube_title.txt'),
                feedin_source=parts[0]
            )

        payload = dict()
        payload['title'] = title
        payload['author'] = 'Caregiver Modern'
        payload['body_html'] = parts[1]
        payload['image'] = dict()
        payload['image']['src'] = image_src
        payload['published'] = 'TRUE'
        
        result = firebase_storage_instance.upload_scheduled_post(
            PostingPlatform.SHOPIFY, 
            payload
        )
        print(result)
    except Exception as e:
        print(f'Something went wrong parsing blog {e}')    
        