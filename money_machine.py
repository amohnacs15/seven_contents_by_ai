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

meta_post_content.sendIgImagePost("", "sample post right here to make sure it all works with new token")
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
    # gpt.source_to_content(filename, summary_ouput, 'prompts/instagram.txt', "Instagram", meta_post_content.sendIgImagePost)
    # gpt.source_to_content(filename, summary_ouput, 'prompts/facebook.txt', "Facebook", meta_post_content.sendFbImagePost)
    # gpt.source_to_content(filename, summary_ouput, 'prompts/linkedin.txt', "LinkedIn", emptyWithParam)
    # gpt.source_to_content(filename, summary_ouput, 'prompts/tweetstorm.txt', "TweetStorm", twitter_post_content.sendTweet)
    # gpt.source_to_content(filename, summary_ouput, 'prompts/email.txt', "Email", emptyWithParam)
    # gpt.source_to_content(filename, summary_ouput, 'prompts/visual.txt', "visual", emptyWithParam)
    # gpt.source_to_content(filename, summary_ouput, 'prompts/takeaways.txt', "takeaways", emptyWithParam)
    # gpt.source_to_content(filename, summary_ouput, 'prompts/script.txt', "youtubescript", emptyWithParam)
    # gpt.source_to_content(filename, summary_ouput, 'prompts/story.txt', "story", emptyWithParam)
    
    