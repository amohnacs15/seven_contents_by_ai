from __future__ import unicode_literals

import argparse

import appsecrets
import meta_graph_api.meta_post_content as meta_post_content 
import text_posts.shopify_blog_content as shopify_blog_content
import media.image_creator as image_creator
import ai.gpt as gpt
import text_posts.twitter_post_content as twitter_post_content
import storage.dropbox_upload as dropbox_upload
from ai.gpt_write_story import create_story_and_scenes
import media.video_editor as video_editor
import media.video_downloader as video_downloader
import media.youtube_uploader as youtube_uploader

#placeholder
def emptyWithParam( init, default ):
    ""
    # print("hit dummy upload")

# Initializations

parser = argparse.ArgumentParser()
parser.add_argument("-url", "--parse_url", help="Youtube video to parse")
args = parser.parse_args()
youtube_url = args.parse_url

print("\n\n")
print("Let's make some money...")
print("\n\n")

# dbx = dropbox_upload.initialize_dropbox()       
# shopify = shopify_blog_content.initialize_shopify()

# filename = video_downloader.save_to_mp3(youtube_url)
# transcriptname = gpt.mp3_to_transcript(filename)

#MAIN FUNCTION
if __name__ == '__main__':
    summary_ouput = 'outputs/summary_output.txt'
    # gpt.transcript_to_summary(transcriptname, filename)

    # filename = 'Private Wojtek, the war bear - One Minute History-vkFLdy5Aico.mp3'
    
    # gpt.source_to_content(filename, transcriptname, 'input_prompts/blog.txt', "blog", shopify_blog_content.upload_shopify_blog_article)
    # gpt.source_to_content(filename, summary_ouput, 'input_prompts/instagram.txt', "instagram", meta_post_content.send_ig_image_post)
    # gpt.source_to_content(filename, summary_ouput, 'input_prompts/facebook.txt', "facebook", meta_post_content.send_fb_image_post)
    # gpt.source_to_content(filename, summary_ouput, 'input_prompts/tweetstorm.txt', "tweetstorm", twitter_post_content.send_tweet)
    gpt.source_to_content(filename, summary_ouput, 'input_prompts/story.txt', 'story', create_story_and_scenes)

    print('\n Movie is in production, Mr. Director... \n')
    # video_remote_url = video_editor.edit_movie_for_remote_url()
    # video_remote_url = 'https://assets.json2video.com/clients/x3hmo82z83/renders/2023-02-09-34066.mp4'
    print('\n Video finished processing. Releasing to cinemas. \n')
    # print(video_remote_url)

    # generated_movie_download_local_path = video_downloader.save_to_video(video_remote_url)
    generated_movie_download_local_path = "output_downloads\\2023-02-09-34066-2023-02-09-34066.mp4"
    youtube_uploader.upload_video_to_youtube(generated_movie_download_local_path)

    # gpt.source_to_content(filename, summary_ouput, 'input_prompts/email.txt', "email", prepareFileForUpload)
    # gpt.source_to_content(filename, summary_ouput, 'input_prompts/script.txt', "youtubescript", youtube.prepareFileForUpload)
    
    # on hold
    # gpt.source_to_content(filename, summary_ouput, 'input_prompts/linkedin.txt', "linkedin", emptyWithParam)