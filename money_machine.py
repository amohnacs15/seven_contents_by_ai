from __future__ import unicode_literals

import argparse

import appsecrets
import meta_graph_api.meta_post_content as meta_post_content 
import text_posts.shopify_blog_content as shopify_blog_content
import media.image_creator as image_creator
import ai.gpt as gpt
import text_posts.twitter_post_content as twitter_post_content
import storage.dropbox_uploader as dropbox_upload
from ai.gpt_write_story import create_story_and_scenes
import media.video_editor as video_editor
import media.video_downloader as video_downloader
import storage.youtube_uploader as youtube_uploader
import ai.gpt as gpt3

dbx = dropbox_upload.initialize_dropbox()       
shopify = shopify_blog_content.initialize_shopify()

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

    filename = video_downloader.save_to_mp3(youtube_url)
    transcriptname = gpt.mp3_to_transcript(filename)
    summary_ouput_file = 'outputs/summary_output.txt'

    gpt.transcript_to_summary(transcriptname, filename)
    
    gpt.prompt_to_file(transcriptname, 'input_prompts/blog.txt', "blog", shopify_blog_content.upload_shopify_blog_article)
    gpt.prompt_to_file(summary_ouput_file, 'input_prompts/instagram.txt', "instagram", meta_post_content.send_ig_image_post)
    gpt.prompt_to_file(summary_ouput_file, 'input_prompts/facebook.txt', "facebook", meta_post_content.send_fb_image_post)
    gpt.prompt_to_file(summary_ouput_file, 'input_prompts/tweetstorm.txt', "tweetstorm", twitter_post_content.send_tweet)
    
    #story must be generated before movie
    gpt.prompt_to_file(summary_ouput_file, 'input_prompts/story.txt', 'story', create_story_and_scenes)
    video_remote_url = video_editor.edit_movie_for_remote_url()
    generated_movie_download_local_path = video_downloader.save_to_video(video_remote_url)
    youtube_uploader.upload_video_to_youtube(generated_movie_download_local_path)
    
    # gpt.prompt_to_file_upload(filename, summary_ouput_file, 'input_prompts/email.txt', "email")
    # gpt.prompt_to_file_upload(filename, summary_ouput_file, 'input_prompts/linkedin.txt', "linkedin")

    