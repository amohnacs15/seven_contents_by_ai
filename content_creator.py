from __future__ import unicode_literals

import argparse

import appsecrets
import meta_graph_api.meta_post_content as meta_post_content 
import text_posts.shopify_blogger as shopify_blogger
import media.image_creator as image_creator
import ai.gpt as gpt
import text_posts.tweeter as tweeter
import storage.dropbox_uploader as dropbox_upload
from ai.gpt_write_story import create_story_and_scenes
import media.video_editor as video_editor
import media.video_downloader as video_downloader
import storage.youtube_uploader as youtube_uploader
import ai.gpt as gpt3
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Initializations
dbx = dropbox_upload.initialize_dropbox()       
shopify = shopify_blogger.initialize_shopify()
firestore_app = firebase_admin.initialize_app()
db = firestore.client()

# Functionality
def create_story_video():
    gpt.prompt_to_file(summary_ouput_file, 'input_prompts/story.txt', 'story', create_story_and_scenes)
    video_remote_url = video_editor.edit_movie_for_remote_url()
    return video_remote_url

def upload_youtube_video( url_path ):    
    generated_movie_download_local_path = video_downloader.save_to_video(url_path)
    youtube_uploader.upload_video_to_youtube(generated_movie_download_local_path)

#MAIN FUNCTION
if __name__ == '__main__':
    # Begin the running of our application
    parser = argparse.ArgumentParser()
    parser.add_argument("-url", "--parse_url", help="Youtube video to parse")
    args = parser.parse_args()
    youtube_url = args.parse_url

    print("\n")
    print("Let's make some money...")
    print("\n")

    # filename = video_downloader.save_to_mp3(youtube_url)
    # transcriptname = gpt.mp3_to_transcript(filename)
    summary_ouput_file = 'outputs/summary_output.txt'

    # gpt.transcript_to_summary(transcriptname, filename)
    
    # gpt.prompt_to_file(transcriptname, 'input_prompts/blog.txt', "blog", shopify_blog_content.upload_shopify_blog_article)
    # gpt.prompt_to_file(summary_ouput_file, 'input_prompts/instagram.txt', "instagram", meta_post_content.send_ig_image_post)
    # gpt.prompt_to_file(summary_ouput_file, 'input_prompts/facebook.txt', "facebook", meta_post_content.send_fb_image_post)
    # gpt.prompt_to_file(summary_ouput_file, 'input_prompts/tweetstorm.txt', "tweetstorm", twitter_post_content.send_tweet)
    
    # video_remote_url = create_story_video()
    # upload_youtube_video(video_remote_url)
    
    # gpt.prompt_to_file_upload(filename, summary_ouput_file, 'input_prompts/email.txt', "email")
    # gpt.prompt_to_file_upload(filename, summary_ouput_file, 'input_prompts/linkedin.txt', "linkedin")
