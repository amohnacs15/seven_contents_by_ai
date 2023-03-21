from __future__ import unicode_literals

import sys
import os
sys.path.append("../src")

import ai.gpt as gpt
import storage.dropbox_uploader as dropbox_upload
import content.ig_content_repo as ig_content_repo
import content.fb_content_repo as fb_content_repo
import content.shopify_content_repo as shopify_content_repo
import content.twitter_content_repo as twitter_content_repo
import gspread

CLIENT_SECRET_FILE='ai-content-machine-d8dcc1434069.json'

def post(type, post_fun): 
    successful_post = post_fun
    print(f'{type} post processed.  Result: {successful_post}')

def get_google_sheets():
    file_path=os.path.join('src', CLIENT_SECRET_FILE)
    sa = gspread.service_account(filename=file_path)  
    sh = sa.open('AI Content Machine')  
    return sh    

# Begin the running of our application
if __name__ == '__main__':
    # Quickly process our posts
    # put our post calls here. this will need to be first with the proper implementation
    post('Shopify', shopify_content_repo.post_shopify_blog_article())
    # post('Facebook', fb_content_repo.post_fb_image())
    # post('Instagram', ig_content_repo.post_ig_media_post())
    # post('Twitter', twitter_content_repo.post_tweet())
    # post_youtube_video()

    # Begin our block for long running creation
    # Schedule our content by iterating through each row of sheet
    sh=get_google_sheets()
    sheet=sh.worksheet("Sheet1")
    cell_list=sheet.get_all_values()

    # we don't want to tax OpenAI. Process one per run
    has_processed_row = False

    for i, row in enumerate(cell_list):
        # if we do not find the word 'Scheduled' in the row, 
        # then we have not processed it yet
        # take action on the row
        if (row.count('Scheduled') == 0 and has_processed_row == False):
            print(f"Processing Row {i}: {row}")
            content_summary = row[0]
            content_description = row[1]

            try:
                gpt.gpt_generate_summary(content_summary)
                 
                # FACEBOOK 
                gpt.generate_prompt_response(
                    prompt_source = os.path.join('src', 'input_prompts', 'facebook.txt'),
                    image_query_term = content_description, 
                    should_polish_post=True,
                    post_num=2,
                    upload_func = fb_content_repo.schedule_fb_post
                )
                # INSTAGRAM
                gpt.generate_prompt_response(
                    prompt_source=os.path.join('src', 'input_prompts', 'instagram.txt'),
                    image_query_term=content_description,
                    should_polish_post=True,
                    post_num=2,
                    upload_func=ig_content_repo.schedule_ig_image_post
                )
                # BLOG AND PROMOS
                gpt.generate_prompt_response(
                    prompt_source=os.path.join('src', 'input_prompts', 'blog.txt'),
                    image_query_term=content_description,
                    should_polish_post=False,
                    post_num=1,
                    upload_func=shopify_content_repo.schedule_shopify_blog_article
                )
                # TWEETS
                gpt.generate_prompt_response(
                    prompt_source=os.path.join('src', 'input_prompts', 'tweetstorm.txt'),
                    image_query_term=content_description,
                    should_polish_post=True,
                    post_num=16,
                    upload_func=twitter_content_repo.schedule_tweet
                )
                # updated cell is the length of the row + 1. check if last cell is empty before updating
                last_cell = sheet.cell(i+1, len(row))
                if (last_cell.value is None or last_cell.value == ''):
                    has_processed_row = True
                    success_value = 'Scheduled'

                    sheet.update_cell(i+1, len(row), success_value)
                    
                    print('Finished as SUCCESS')
            except Exception as e:
                print(f'Finished with error {e}')        
    print('Finished and completed')
    
# Stalled 
    # process_initial_video_download_transcript(content_summary)  
    # schedule_video_story(content_description)

    # upload these to dropbox
    # gpt.prompt_to_file_upload(filename, summary_ouput_file, 'input_prompts/email.txt', "email")
    # gpt.prompt_to_file_upload(filename, summary_ouput_file, 'input_prompts/linkedin.txt', "linkedin")
    
    # v2 instagram video just needs a time and a place
    # file_path = os.path.join("src", "outputs", "instagram_output.txt")
    # gpt.prompt_to_file(summary_output_file, 'instagram_video', video_remote_url, ig_content_repo.schedule_ig_video_post)    