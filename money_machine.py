from __future__ import unicode_literals

import youtube_dl
import whisper
import warnings
import ffmpeg
import os
import numpy
warnings.filterwarnings("ignore")
import openai
from time import time,sleep
import textwrap
import re
import pathlib
import pandas as pd
import dropbox
from dropbox.exceptions import AuthError
import tweepy
import replicate
import shopify
import requests
import urllib.parse
import json
import argparse

import appsecrets
from ig_debug_token import getIgDebugAccessToken
from ig_post_content import sendIgImagePost, sendIgVideoPost








# UTILITY

def open_url(url):
    '''
    Function to Open URL.
    Used to open the authorization link
    '''
    import webbrowser
    print(url)
    webbrowser.open(url)

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def remove_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
    else:
        print("Deletion Failed: The file does not exist")        

# Original 7 content functions
#GPT-3 Function        
def gpt_3 (prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1.2,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    text = response['choices'][0]['text'].strip()
    return text

#Download YouTube Video        
def save_to_mp3(url):
    """Save a YouTube video URL to mp3.

    Args:
       # url (str): A YouTube video URL.

    Returns:
        #str: The filename of the mp3 file.
    """

    options = {
        'outtmpl': 'downloads/%(title)s-%(id)s.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'nocheckcertificate': True
     }

    with youtube_dl.YoutubeDL(options) as downloader:
        downloader.download(["" + url + ""])
                
        return downloader.prepare_filename(downloader.extract_info(url, download=False)).replace(".m4a", ".mp3").replace(".webm", ".mp3")

# Access mp3 on Desktop with Pathfolder
    # desktop_path = "/Users/adrian.mohnacs/Python/YTcontent/"
    # folder_name = "YTcontent"
    # file_name = 'ytyt.mp3'
    # file_path = os.path.join(desktop_path, filename)
    # sound = file_path 

def mp3_to_transcript(mp3_filename):
    sound = mp3_filename
    model = whisper.load_model("medium")
    result = model.transcribe(sound, fp16=False)
    yttrans = (result['text'])
    # print(yttrans)
    result_path = filename + '_transcript.txt'
    save_file(result_path, yttrans)
    return result_path

def transcript_to_summary(transcriptname, filename):
    alltext = open_file(transcriptname)
    chunks = textwrap.wrap(alltext, 2500)
    result = list()
    count = 0
    for chunk in chunks:
        count = count + 1
        prompt = open_file('prompts/summary.txt').replace('<<SUMMARY>>', chunk)
        prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
        summary = gpt_3(prompt)
        print('\n\n\n', count, 'out of', len(chunks), 'Compressions', ' : ', summary)
        result.append(summary)
    save_file('outputs/summary_output.txt', '\n\n'.join(result))

def source_to_content(filename, feedin_source, prompt_source, type, upload_func):
        """Convert a single file of language to another using chat GPT and upload to dropbox
        
        Args:
        feedin_source (str): The path to the file.
        prompt_source (str): The path for the GPT prompt.
        type (str): simple categorization to help with naming
        dropbox_file_path (str): The path to the file in the Dropbox app directory.

        Example:
            dropbox_upload_file('.', 'test.csv', '/stuff/test.csv')

        Returns: nothing
        """
        feedin = open_file(feedin_source)
        appliedprompt = open_file(prompt_source).replace('<<FEED>>', feedin)
        finaltext = gpt_3(appliedprompt)
        
        print('\n\n\n', type + ' post:\n\n', finaltext)

        saveFilePath = 'outputs/'+type+'_output.txt'

        save_file(saveFilePath, finaltext)
        upload_func(saveFilePath, finaltext)
        # dropbox_upload_file(saveFilePath, '/' + filename.replace(".mp3", "") + '/' + type + '_output.txt')
        # remove_file(saveFilePath)







#DROPBOX 

def initialize_dropbox():
        """Create a connection to Dropbox."""
        try:
            dbx = dropbox.Dropbox(appsecrets.DROPBOX_APP_TOKEN)
            print('Dropbox Initialized Successfully')
        except AuthError as e:
            print('Error Connecting to Dropbox')
        return dbx

def dropbox_upload_file(local_path, local_file, dropbox_file_path):
    """Upload a file from the local machine to a path in the Dropbox app directory.

    Args:
        local_path (str): The path to the local file.
        local_file (str): The name of the local file.
        dropbox_file_path (str): The path to the file in the Dropbox app directory.

    Example:
        source_to_content(filename, transcriptname, 'prompts/blog.txt', "blog")

    Returns:
        meta: The Dropbox file metadata.
    """

    try:
        # dbx = dropbox_connect()
        local_file_path = pathlib.Path(local_path) / local_file

        with local_file_path.open("rb") as f:
            meta = dbx.files_upload(f.read(), dropbox_file_path, mode=dropbox.files.WriteMode("overwrite"))

            print("Upload success of " + local_file)

            return meta
    except Exception as e:
        print('Error uploading file to Dropbox: ' + str(e))          








# TWITTER
def initialize_tweepy():
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(appsecrets.TWITTER_API_KEY, appsecrets.TWITTER_API_SECRET)
    auth.set_access_token(appsecrets.TWITTER_API_AUTH_TOKEN, appsecrets.TWITTER_API_AUTH_SECRET)

    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        print("Twitter Authentication OK")
    except:
        print("Error during Tweepy authentication") 
    return api    

def sendTweet(filePath, tweet):
    # Using readlines()
    tweetFile = open(filePath, 'r')
    tweets = tweetFile.readlines()

    # Strips the newline character
    for tweet in tweets:
        if (tweet.strip()):
            print("Tweet sent......." + tweet)
            #tweepy_api.update_status(status = tweet)   

def emptyWithParam(init, default):
    print("hit dummy upload")






#MIDHOURNEY IMAGES

def createMidjourneyImage(visual_prompt, width, height):
    api = replicate.Client(appsecrets.REPLICATE_TOKEN)
    model = api.models.get("tstramer/midjourney-diffusion")
    version = model.versions.get("436b051ebd8f68d23e83d22de5e198e0995357afef113768c20f0b6fcef23c8b")

#     # https://replicate.com/tstramer/midjourney-diffusion/versions/436b051ebd8f68d23e83d22de5e198e0995357afef113768c20f0b6fcef23c8b#input
    inputs = {
#         # Input prompt
        'prompt': "mdjrny-v4 style  pharah from overwatch, character portrait, portrait, close up, concept art, intricate details, highly detailed, vintage sci - fi poster, retro future, in the style of chris foss, rodger dean, moebius, michael whelan, and gustave dore",

#         # Specify things to not see in the output # 'negative_prompt': ...,

#         # Width of output image. Maximum size is 1024x768 or 768x1024 because # of memory limits
        'width': width,

#         # Height of output image. Maximum size is 1024x768 or 768x1024 because of memory limits
        'height': height,

#         # Prompt strength when using init image. 1.0 corresponds to full destruction of information in init image
        'prompt_strength': 0.8,

#         # Number of images to output. # Range: 1 to 4
        'num_outputs': 1,

#         # Number of denoising steps # Range: 1 to 500
        'num_inference_steps': 50,

#         # Scale for classifier-free guidance # Range: 1 to 20
        'guidance_scale': 7.5,

#         # Choose a scheduler.
        'scheduler': "DPMSolverMultistep",

#         # Random seed. Leave blank to randomize the seed
#         # 'seed': ...,
    }

#     # https://replicate.com/tstramer/midjourney-diffusion/versions/436b051ebd8f68d23e83d22de5e198e0995357afef113768c20f0b6fcef23c8b#output-schema
    output = version.predict(**inputs)
    print("midjourney output")
    print(output[0])
    output[0]




















# Shopify Blog Upload
def initialize_shopify():
    # Configure store details
    shop_url = 'osaka-cosplay.myshopify.com'
    admin_api_key = appsecrets.SHOPIFY_ADMIN_API_TOKEN
    api_version = '2023-01'
    # Create and activate a new session
    session = shopify.Session(shop_url, api_version, admin_api_key)
    shopify.ShopifyResource.activate_session(session)

def upload_shopify_blog_article(filePath, blog):
    blogfile = open(filePath, 'r')
    bloglines = blogfile.readlines()

    title = bloglines[0].replace("# H1: ", " ").strip()
    title = bloglines[0].replace("#H1 - ", " ").strip()
    title = bloglines[0].replace("#H1 ", " ").strip()
    title = bloglines[0].replace("#", " ").strip()
    
    new_blog = shopify.Blog.create({"title": title})
    if (new_blog.save()):
        new_article = shopify.Article()

        new_article.title = title
        new_article.author = "Caregiver Modern"
        new_article.blog_id = new_blog.id
        new_article.body_html = blog
        # new_article.image = createMidjourneyImage("default", 1024, 768)
        new_article.published = 'TRUE'
        new_article.save()
        print ("Shopify article upload successful")
    else:
        print (blog.errors.full_messages())

#################End of function. Beginning of execution######################

getIgDebugAccessToken()
# Initializations
openai.api_key = appsecrets.OPEN_AI_API_KEY  

parser = argparse.ArgumentParser()
parser.add_argument("-url", "--parse_url", help="Youtube video to parse")
args = parser.parse_args()
youtube_url = args.parse_url

print("\n\n")
print("Let's make some money...")
print("\n\n")

initialize_shopify()
dbx = initialize_dropbox()       
tweepy_api = initialize_tweepy()

filename = save_to_mp3(youtube_url)
transcriptname = mp3_to_transcript(filename)

#MAIN FUNCTION
if __name__ == '__main__':
    summary_ouput = 'outputs/summary_output.txt'

    transcript_to_summary(transcriptname, filename)
    
    # source_to_content(filename, transcriptname, 'prompts/blog.txt', "Blog", upload_shopify_blog_article)
    # source_to_content(filename, summary_ouput, 'prompts/instagram_facebook.txt', "Instagram", sendIgImagePost)
    # source_to_content(filename, summary_ouput, 'prompts/linkedin.txt', "LinkedIn", emptyWithParam)
    # source_to_content(filename, summary_ouput, 'prompts/tweetstorm.txt', "TweetStorm", sendTweet)
    # source_to_content(filename, summary_ouput, 'prompts/email.txt', "Email", emptyWithParam)
    # source_to_content(filename, summary_ouput, 'prompts/visual.txt', "visual", emptyWithParam)
    # source_to_content(filename, summary_ouput, 'prompts/takeaways.txt', "takeaways", emptyWithParam)
    # source_to_content(filename, summary_ouput, 'prompts/script.txt', "youtubescript", emptyWithParam)
    # source_to_content(filename, summary_ouput, 'prompts/story.txt', "story", emptyWithParam)
    # source_to_content(filename, summary_ouput, 'prompts/quiz.txt', "quiz", emptyWithParam)
    
    