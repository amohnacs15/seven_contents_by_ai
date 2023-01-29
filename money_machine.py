from __future__ import unicode_literals

import argparse

import appsecrets
import ig_debug_token
import ig_post_content 
import shopify_blog_content
import image_creation
import gpt
import twitter_post_content
import dropbox_upload

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

ig_debug_token.getIgDebugAccessToken()
shopify_blog_content.initialize_shopify()
dbx = dropbox_upload.initialize_dropbox()       
tweepy_api = twitter_post_content.initialize_tweepy()

# filename = gpt.save_to_mp3(youtube_url)
# transcriptname = gpt.mp3_to_transcript(filename)

#MAIN FUNCTION
if __name__ == '__main__':
    summary_ouput = 'outputs/summary_output.txt'

    # gpt.transcript_to_summary(transcriptname, filename)
    
    # gpt.source_to_content(filename, transcriptname, 'prompts/blog.txt', "Blog", shopify_blog_content.upload_shopify_blog_article)
    # gpt.source_to_content(filename, summary_ouput, 'prompts/instagram_facebook.txt', "Instagram", ig_post_content.sendIgImagePost)
    # gpt.source_to_content(filename, summary_ouput, 'prompts/linkedin.txt', "LinkedIn", emptyWithParam)
    # gpt.source_to_content(filename, summary_ouput, 'prompts/tweetstorm.txt', "TweetStorm", twitter_post_content.sendTweet)
    # gpt.source_to_content(filename, summary_ouput, 'prompts/email.txt', "Email", emptyWithParam)
    # gpt.source_to_content(filename, summary_ouput, 'prompts/visual.txt', "visual", emptyWithParam)
    # gpt.source_to_content(filename, summary_ouput, 'prompts/takeaways.txt', "takeaways", emptyWithParam)
    # gpt.source_to_content(filename, summary_ouput, 'prompts/script.txt', "youtubescript", emptyWithParam)
    # gpt.source_to_content(filename, summary_ouput, 'prompts/story.txt', "story", emptyWithParam)
    # gpt.source_to_content(filename, summary_ouput, 'prompts/quiz.txt', "quiz", emptyWithParam)
    
    