from __future__ import unicode_literals

import argparse

import src.ai.gpt as gpt
import src.storage.dropbox_uploader as dropbox_upload
from src.ai.gpt_write_story import create_story_and_scenes
import src.media.video_editor as video_editor
import src.media.video_downloader as video_downloader
import src.storage.youtube_content_repo as youtube_content_repo
import src.meta_graph_api.ig_content_repo as ig_content_repo
import src.utility.utils as utils

# Initializations
dbx = dropbox_upload.initialize_dropbox()      

# Functionality
def create_story_video():
    gpt.prompt_to_file(summary_ouput_file, 'input_prompts/story.txt', 'story', create_story_and_scenes)
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
    # parser.add_argument("-content-desc", "--parse_url", help="query term to be used when generating images and video")
    args = parser.parse_args()
    youtube_url = args.parse_url

    print("\n")
    print("Let's make some money...")
    print("\n")

    # filename = video_downloader.save_to_mp3(youtube_url)
    # transcriptname = gpt.mp3_to_transcript(filename)
    summary_ouput_file = 'src/outputs/summary_output.txt'

    # gpt.transcript_to_summary(transcriptname, filename)

    # creating our post objects and scheduling them with our remote application
    
    # gpt.prompt_to_file(transcriptname, 'input_prompts/blog.txt', "blog", shopify_blog_content.upload_shopify_blog_article)
    # gpt.prompt_to_file(summary_ouput_file, 'input_prompts/instagram.txt', "instagram", meta_post_content.send_ig_image_post)
    
    # ig_content_repo.schedule_ig_image_post(utils.open_file('outputs/instagram_output.txt'), 'elderly')
    ig_content_repo.schedule_ig_video_post(utils.open_file('src/outputs/instagram_output.txt'))

    #gpt3.prompt_to_file(fb_content_repo.schedule_fb_post('output file'), 'elderly')

    # gpt3.prompt_to_file(summary_ouput_file, 'input_prompts/facebook.txt', "facebook", fb_content_repo.schedule_facebook_post)    
    # gpt.prompt_to_file(summary_ouput_file, 'input_prompts/tweetstorm.txt', "tweetstorm", twitter_post_content.send_tweet)
    
    # video_remote_url = create_story_video()
    # upload_youtube_video(video_remote_url)

    
    # gpt.prompt_to_file_upload(filename, summary_ouput_file, 'input_prompts/email.txt', "email")
    # gpt.prompt_to_file_upload(filename, summary_ouput_file, 'input_prompts/linkedin.txt', "linkedin")
