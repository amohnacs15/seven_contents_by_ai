from __future__ import unicode_literals

import sys
import os
sys.path.append("../src")

import argparse

import ai.gpt as gpt
import storage.dropbox_uploader as dropbox_upload
from ai.gpt_write_story import create_story_and_scenes
import media.video_editor as video_editor
import media.video_downloader as video_downloader
import storage.youtube_content_repo as youtube_content_repo
import meta_graph_api.ig_content_repo as ig_content_repo
import meta_graph_api.fb_content_repo as fb_content_repo
import utility.utils as utils
import text_posts.shopify_content_repo as shopify_content_repo
import text_posts.twitter_content_repo as tweet_repo

# Initializations
dbx = dropbox_upload.initialize_dropbox() 
shopify_content_repo.initialize_shopify()     

# Functionality
def process_initial_video_download(youtube_url):
    filename = video_downloader.save_to_mp3(youtube_url)
    transcriptname = gpt.mp3_to_transcript(filename)
    gpt.transcript_to_summary(transcriptname, filename) 

def create_story_video_url():
    file_path = os.path.join("src", "input_prompts", "story.txt")
    gpt.prompt_to_file(file_path, 'story', create_story_and_scenes)
    video_remote_url = video_editor.edit_movie_for_remote_url()
    return video_remote_url

# Begin the running of our application
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-url", "--parse_url", help="Youtube video to parse")
    parser.add_argument("-content-desc", "--content_desc", help="query term to be used when generating images and video")
    args = parser.parse_args()

    youtube_url = args.parse_url
    content_description = args.content_desc

    print("\n")
    print("I will be wealthy...")
    print("\n")

    process_initial_video_download(youtube_url)
    
 # preliminary input completed   
    video_remote_url = create_story_video_url()
    youtube_content_repo.schedule_youtube_video(video_remote_url)

# Stalled 
    # upload these to dropbox
    # gpt.prompt_to_file_upload(filename, summary_ouput_file, 'input_prompts/email.txt', "email")
    # gpt.prompt_to_file_upload(filename, summary_ouput_file, 'input_prompts/linkedin.txt', "linkedin")
    
    # instagram video just needs a time and a place
    # file_path = os.path.join("src", "outputs", "instagram_output.txt")
    # gpt.prompt_to_file(summary_output_file, 'instagram_video', video_remote_url, ig_content_repo.schedule_ig_video_post)

# completely done and ready to be scheduled
    # gpt.prompt_to_file(
    #     type = 'facebook', 
    #     prompt_source = os.path.join('src', 'outputs', 'facebook_output.txt')
    #     image_query_term = content_description, 
    #     upload_func = fb_content_repo.schedule_fb_post
    # )
    # gpt.prompt_to_file(
    #     type='instagram', 
    #     prompt_source=os.path.join('src', 'outputs', 'instagram_output.txt')
    #     image_query_term=content_description,
    #     upload_func=ig_content_repo.schedule_ig_image_post
    # )
    # gpt.prompt_to_file(
    #     type="shopify_blog", 
    #     prompt_source=os.path.join('src', 'outputs', 'shopify_blog_output.txt'),
    #     image_query_term=content_description,
    #     upload_func=shopify_content_repo.schedule_shopify_blog_article
    # )
    # gpt.prompt_to_file(
    #     type='tweestorm',
    #     prompt_source=os.path.join('src', 'input_prompts', 'tweetstorm.txt'),
    #     image_query_term=content_description,
    #     upload_func=tweet_repo.schedule_tweets
    # )