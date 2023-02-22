from __future__ import unicode_literals

import sys
import os
sys.path.append("../src")

import gspread
import ai.gpt as gpt
import storage.dropbox_uploader as dropbox_upload
from ai.gpt_write_story import create_story_and_scenes
import media.video_editor as video_editor
import media.video_downloader as video_downloader
import storage.youtube_content_repo as youtube_content_repo
import meta_graph_api.ig_content_repo as ig_content_repo
import meta_graph_api.fb_content_repo as fb_content_repo
import text_posts.shopify_content_repo as shopify_content_repo
import text_posts.twitter_content_repo as twitter_content_repo

CLIENT_SECRET_FILE='ai-content-machine-d8dcc1434069.json'

# Initializations
dbx = dropbox_upload.initialize_dropbox() 
shopify = shopify_content_repo.initialize_shopify()

# Posting Functionality
def post(type, post_fun): 
    successful_post = post_fun
    print(f'{type} post processed.  Result: {successful_post}')

def post_youtube_video():    
    response = youtube_content_repo.post_upload_video_to_youtube()
    print(response) 

# Scheduling Functionality
def process_initial_video_download_transcript(youtube_url):
    filename = video_downloader.save_to_mp3(youtube_url)
    transcriptname = gpt.mp3_to_transcript(filename)
    gpt.transcript_to_summary(transcriptname, filename) 

def schedule_video_story():
    file_path = os.path.join("src", "input_prompts", "story.txt")
    gpt.prompt_to_file(
        prompt_source=file_path, 
        type='story', 
        image_query_term='old',
        upload_func=create_story_and_scenes
    )
    video_remote_url = video_editor.edit_movie_for_remote_url()
    result = youtube_content_repo.schedule_youtube_video(video_remote_url)
    print(f'youtube schedule result\n\n{result}')

def get_google_sheets():
    file_path=os.path.join('src', CLIENT_SECRET_FILE)
    sa = gspread.service_account(filename=file_path)  
    sh = sa.open('AI Content Machine')  
    return sh

# Begin the running of our application
if __name__ == '__main__':

    print("\n")
    print("Starting content generation...")
    print("\n")

    # Quickly process our posts
    # put our post calls here. this will need to be first with the proper implementation
    # post('Shopify', shopify_content_repo.post_shopify_blog_article())
    post('Facebook', fb_content_repo.post_fb_image())
    post('Instagram', ig_content_repo.post_ig_media_post())
    post('Twitter', twitter_content_repo.post_tweet())
    post_youtube_video()
     
    # Iterate through each row of sheet
    sh=get_google_sheets()
    sheet=sh.worksheet("Sheet1")
    cell_list=sheet.get_all_values()

    for i, row in enumerate(cell_list):
        if (row.count('Scheduled') == 0):
            # Take action on the row
            # For example, print the values of each cell in the row
            print(f"Processing Row {i+1}: {row}")
            youtube_url = row[0]
            content_description = row[1]

            # download the video, convert to mp3, and generate a transcript
            process_initial_video_download_transcript(youtube_url)

            # begin our block for long running creation
            gpt.prompt_to_file(
                type = 'facebook', 
                prompt_source = os.path.join('src', 'input_prompts', 'facebook.txt'),
                image_query_term = content_description, 
                upload_func = fb_content_repo.schedule_fb_post
            )
            gpt.prompt_to_file(
                type='instagram', 
                prompt_source=os.path.join('src', 'input_prompts', 'instagram.txt'),
                image_query_term=content_description,
                upload_func=ig_content_repo.schedule_ig_image_post
            )
            gpt.prompt_to_file(
                type="shopify_blog", 
                prompt_source=os.path.join('src', 'input_prompts', 'blog.txt'),
                image_query_term=content_description,
                upload_func=shopify_content_repo.schedule_shopify_blog_article
            )
            gpt.prompt_to_file(
                type='tweetstorm',
                prompt_source=os.path.join('src', 'input_prompts', 'tweetstorm.txt'),
                image_query_term=content_description,
                upload_func=twitter_content_repo.schedule_tweets
            )
            schedule_video_story()

            # updated cell is the length of the row + 1
            success_value = 'Scheduled'
            sheet.update_cell(i+1, len(row)+1, success_value)

# Stalled 
    # upload these to dropbox
    # gpt.prompt_to_file_upload(filename, summary_ouput_file, 'input_prompts/email.txt', "email")
    # gpt.prompt_to_file_upload(filename, summary_ouput_file, 'input_prompts/linkedin.txt', "linkedin")
    
    # v2 instagram video just needs a time and a place
    # file_path = os.path.join("src", "outputs", "instagram_output.txt")
    # gpt.prompt_to_file(summary_output_file, 'instagram_video', video_remote_url, ig_content_repo.schedule_ig_video_post)    