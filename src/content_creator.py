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
import utility.utils as utils

# Initializations
dbx = dropbox_upload.initialize_dropbox()      

# Functionality
def create_story_video():
    file_path = os.path.join("src", "input_prompts", "story.txt")
    gpt.prompt_to_file(summary_ouput_file, file_path, 'story', create_story_and_scenes)
    video_remote_url = video_editor.edit_movie_for_remote_url()
    return video_remote_url

def upload_youtube_video( url_path ):    
    generated_movie_download_local_path = video_downloader.save_to_video(url_path)
    youtube_content_repo.upload_video_to_youtube(generated_movie_download_local_path)

#MAIN FUNCTION
if __name__ == '__main__':
    # Begin the running of our application
    parser = argparse.ArgumentParser()
    parser.add_argument("-url", "--parse_url", help="Youtube video to parse")
    parser.add_argument("-content-desc", "--content_desc", help="query term to be used when generating images and video")
    args = parser.parse_args()
    youtube_url = args.parse_url
    content_description = args.content_desc

    print("\n")
    print("Let's make some money...")
    print("\n")

    # filename = video_downloader.save_to_mp3(youtube_url)
    # transcriptname = gpt.mp3_to_transcript(filename)
    summary_ouput_file = os.path.join("src", "outputs", "summary_output.txt")

    # gpt.transcript_to_summary(transcriptname, filename)

    # creating our post objects and scheduling them with our remote application
    
    # gpt.prompt_to_file(transcriptname, 'input_prompts/blog.txt', "blog", shopify_blog_content.upload_shopify_blog_article)
    # gpt.prompt_to_file(summary_ouput_file, 'input_prompts/instagram.txt', "instagram", meta_post_content.send_ig_image_post)
    
    # gpt3.prompt_to_file(summary_ouput_file, 'input_prompts/facebook.txt', "facebook", fb_content_repo.schedule_facebook_post)    
    # gpt.prompt_to_file(summary_ouput_file, 'input_prompts/tweetstorm.txt', "tweetstorm", twitter_post_content.send_tweet)
 
 # preliminary done   
    # video_remote_url = create_story_video()
    # upload_youtube_video(video_remote_url)
    # file_path = os.path.join("src", "outputs", "instagram_output.txt")
    # gpt.prompt_to_file(summary_output_file, 'instagram_video', video_remote_url, ig_content_repo.schedule_ig_video_post)

# Stalled for remote upload to Dropbox
    # gpt.prompt_to_file_upload(filename, summary_ouput_file, 'input_prompts/email.txt', "email")
    # gpt.prompt_to_file_upload(filename, summary_ouput_file, 'input_prompts/linkedin.txt', "linkedin")

# completely done and ready to be scheduled
    #gpt.prompt_to_file(summary_output_file, 'facebook', content_description, fb_content_repo.schedule_fb_post)
    #gpt.prompt_to_file(summary_output_file, 'instagram_image', content_description,ig_content_repo.schedule_ig_image_post)