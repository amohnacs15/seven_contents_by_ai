from __future__ import unicode_literals

import argparse

import appsecrets
import meta_tokens as meta_tokens
import meta_graph_api.meta_post_content as meta_post_content 
import text_posts.shopify_blog_content as shopify_blog_content
import media.image_creator as image_creator
import ai.gpt as gpt
import text_posts.twitter_post_content as twitter_post_content
import uploads.dropbox_upload as dropbox_upload
from ai.gpt_write_story import create_story_and_scenes
import ai.speech_synthesis as speech_syn
import media.video_editor as video_editor
import media.video_downloader as video_downloads

#placeholder
def emptyWithParam( init, default ):
    print("hit dummy upload")

def prepareFileForUpload( filename, input ):   
    first_word = input.split()[0]
    dropbox_location = '/' + filename.replace(".mp3", "") + '/' + first_word + '.txt'
    dbx.drop_upload_file( dbx, filename, dropbox_location)

# Initializations

parser = argparse.ArgumentParser()
parser.add_argument("-url", "--parse_url", help="Youtube video to parse")
args = parser.parse_args()
youtube_url = args.parse_url

print("\n\n")
print("Let's make some money...")
print("\n\n")


# dbx = dropbox_upload.initialize_dropbox()       
# tweepy_api = twitter_post_content.initialize_tweepy()
# shopify = shopify_blog_content.initialize_shopify()

# filename = video_downloads.save_to_mp3(youtube_url)
# transcriptname = gpt.mp3_to_transcript(filename)


#MAIN FUNCTION
if __name__ == '__main__':
    summary_ouput = 'outputs/summary_output.txt'

    video_editor.getEditedMovie()

    # gpt.transcript_to_summary(transcriptname, filename)
    
    # gpt.source_to_content(filename, transcriptname, 'input_prompts/blog.txt', "blog", shopify_blog_content.upload_shopify_blog_article)
    # gpt.source_to_content(filename, summary_ouput, 'input_prompts/instagram.txt', "instagram", meta_post_content.sendIgImagePost)
    # gpt.source_to_content(filename, summary_ouput, 'input_prompts/facebook.txt', "facebook", meta_post_content.sendFbImagePost)
    # gpt.source_to_content(filename, summary_ouput, 'input_prompts/tweetstorm.txt', "tweetstorm", twitter_post_content.sendTweet)
    # gpt.source_to_content(filename, summary_ouput, 'input_prompts/email.txt', "email", prepareFileForUpload)

    # gpt.source_to_content(filename, summary_ouput, 'input_prompts/script.txt', "youtubescript", prepareFileForUpload)
    
    # on hold
    # gpt.source_to_content(filename, summary_ouput, 'input_prompts/linkedin.txt', "linkedin", emptyWithParam)