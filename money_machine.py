from __future__ import unicode_literals

import argparse

import appsecrets
import meta_tokens as meta_tokens
import meta_graph_api.meta_post_content as meta_post_content 
import text_posts.shopify_blog_content as shopify_blog_content
import media.image_creation as image_creation
import media.gpt as gpt
import text_posts.twitter_post_content as twitter_post_content
import uploads.dropbox_upload as dropbox_upload
from media.gpt_write_story import create_story_and_scenes
import media.speech_synthesis as speech_syn

#placeholder
def emptyWithParam(init, default):
    print("hit dummy upload")

# Initializations

parser = argparse.ArgumentParser()
parser.add_argument("-url", "--parse_url", help="Youtube video to parse")
args = parser.parse_args()
youtube_url = args.parse_url

print("\n\n")
print("Let's make some money...")
print("\n\n")



shopify_blog_content.initialize_shopify()
dbx = dropbox_upload.initialize_dropbox()       
tweepy_api = twitter_post_content.initialize_tweepy()

filename = gpt.save_to_mp3(youtube_url)
transcriptname = gpt.mp3_to_transcript(filename)

#MAIN FUNCTION
if __name__ == '__main__':
    summary_ouput = 'outputs/summary_output.txt'

    gpt.transcript_to_summary(transcriptname, filename)
    
    # gpt.source_to_content(filename, transcriptname, 'input_prompts/blog.txt', "blog", shopify_blog_content.upload_shopify_blog_article)
    # gpt.source_to_content(filename, summary_ouput, 'input_prompts/instagram.txt', "instagram", meta_post_content.sendIgImagePost)
    # gpt.source_to_content(filename, summary_ouput, 'input_prompts/facebook.txt', "facebook", meta_post_content.sendFbImagePost)
    
    # gpt.source_to_content(filename, summary_ouput, 'input_prompts/tweetstorm.txt', "tweetstorm", twitter_post_content.sendTweet)
    # gpt.source_to_content(filename, summary_ouput, 'input_prompts/email.txt', "email", emptyWithParam)
    # gpt.source_to_content(filename, summary_ouput, 'input_prompts/script.txt', "youtubescript", emptyWithParam)
    gpt.source_to_content(filename, summary_ouput, 'input_prompts/story.txt', "story", create_story_and_scenes)
    
    # on hold
    # gpt.source_to_content(filename, summary_ouput, 'input_prompts/linkedin.txt', "linkedin", emptyWithParam)