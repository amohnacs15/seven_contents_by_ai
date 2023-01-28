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
import json
import random
import requests
import string
import argparse
from urllib.parse import urlparse, parse_qs

import appsecrets







# Original 7 content functions
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

def empty_with_param(init, default):
    print("hit dummy upload")








#MIDJOURNEY IMAGES

def get_midjourney_image(visual_prompt, width, height):
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








# SHOPIFY
def initialize_shopify_session():
    # Configure store details
    shop_url = 'osaka-cosplay.myshopify.com'
    admin_api_key = appsecrets.SHOPIFY_ADMIN_API_TOKEN
    api_version = '2023-01'
    # Create and activate a new session
    session = shopify.Session(shop_url, api_version, admin_api_key)
    shopify.ShopifyResource.activate_session(session)
    print("Shopify session active")

def send_shopify_article(filePath, blog):
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
        new_article.published = 'TRUE'
        # new_article.image = createMidjourneyImage("default", 1024, 768)
        # new_article.save()
        print ("Shopify article upload successful")
    else:
        print (blog.errors.full_messages())






#EMAIL
def send_email_to_dropbox(filename, email):
    email.replace('[Business Name]', 'Your Family At Caregiver Modern')
    email.replace('[insert business name]', 'Your Family At Caregiver Modern')
    email.replace('[Your Company]', 'Your Family At Caregiver Modern')
    dropbox_upload_file('outputs', 'Email_output.txt', '/marketing_emails/' + filename.replace(".mp3", ""))
    print("Email successfull uploaded")







#LINKEDIN

def initialize_linkedin(credentials):
    '''
    Run the Authentication.
    If the access token exists, it will use it to skip browser auth.
    If not, it will open the browser for you to authenticate.
    You will have to manually paste the redirect URI in the prompt.
    '''
    creds = read_creds(credentials)
    client_id, client_secret = appsecrets.LINKEDIN_CLIENT_ID, appsecrets.LINKEDIN_CLIENT_SECRET
    redirect_uri = creds['redirect_uri']
    api_url = 'https://www.linkedin.com/oauth/v2'
         
    if 'access_token' not in creds.keys(): 
        print("Generating new LinkedIn access token")
        args = client_id,client_secret,redirect_uri
        auth_code = authorize(api_url,*args)
        access_token = refresh_token(auth_code,*args)
        creds.update({'access_token':access_token})
        save_token(credentials, creds)
    else: 
        access_token = creds['access_token']
    print("LinkedIn access token retrieved")    
    return access_token  

def get_linkedin_headers(access_token):
    '''
    Make the headers to attach to the API call.
    '''
    headers = {
    'Authorization': f'Bearer {access_token}',
    'x-li-src':  'json', 
    'cache-control': 'no-cache',
    'X-Restli-Protocol-Version': '2.0.0'
    }
    return headers

def authorize(api_url, client_id,client_secret,redirect_uri):
    '''
    This function generates a random string of letters.
    It is not required by the Linkedin API to use a CSRF token.
    However, it is recommended to protect against cross-site request forgery
    '''
    letters = string.ascii_lowercase
    csrf_token = ''.join(random.choice(letters) for i in range(20))
 
    '''
    Make a HTTP request to the authorization URL.
    It will open the authentication URL.
    Once authorized, it'll redirect to the redirect URI given.
    The page will look like an error. but it is not.
    You'll need to copy the redirected URL.
    '''
    data = {
        'Content-Type' : 'application/x-www-form-urlencoded',
        'grant_type' : 'client_credentials',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'state': csrf_token,
        'scope': 'w_member_social'
        }
 
    response = requests.post(f'{api_url}/authorization',data=data)
    print(response)
    data = json.loads(str(response))
    auth_code = data['access_token']
    print(auth_code)
    
 
    # print(f'''
    #     The Browser will open to ask you to authorize the credentials.\n
    #     Since we have not set up a server, you will get the error:\n
    #     This site can’t be reached. localhost refused to connect.\n
    #     This is normal.\n
    #     You need to copy the URL where you are being redirected to.\n
    #     '''
    # )
 
    # open_url(response.url)
 
    # Get the authorization verifier code from the callback url, where it says "code?"
    # auth_code = input('Paste the access code paramter here:')

    return auth_code

def refresh_token(auth_code,client_id,client_secret,redirect_uri):
    '''
    Exchange a Refresh Token for a New Access Token.
    '''
    access_token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
 
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
        }
 
    response = requests.post(access_token_url, data=data, timeout=30)
    response = response.json()
    access_token = response['access_token']
    return access_token   

def save_token(filename,data):
    '''
    Write token to credentials file.
    '''
    data = json.dumps(data, indent = 4) 
    with open(filename, 'w') as f: 
        f.write(data)      

def open_url(url):
    '''
    Function to Open URL.
    Used to open the authorization link
    '''
    import webbrowser
    print(url)
    webbrowser.open(url)

def parse_redirect_uri(redirect_response):
    '''
    Parse redirect response into components.
    Extract the authorized token from the redirect uri.
    '''
    
    url = urlparse(redirect_response)
    url = parse_qs(url.query)
    return url['code'][0]

def read_creds(filename):
    '''
    Store API credentials in a safe place.
    If you use Git, make sure to add the file to .gitignore
    '''
    with open(filename) as f:
        credentials = json.load(f)
    return credentials

def get_author(headers):
    '''
    Get user information from Linkedin
    '''
    response = requests.get('https://api.linkedin.com/v2/me', headers = headers)
    user_info = response.json()
    
    # Get user id to make a UGC post
    urn = user_info['id']
    author = f'urn:li:person:{urn}'
    return author

def linkedin_post_data(author, post):
    message = 'Preparing a LinkedIn Bot'

    link = 'https://www.jcchouinard.com/how-to-use-the-linkedin-api-python/'
    link_text = 'Complete tutorial using the LinkedIn API'
    
    post_data = {
        "author": "Caregiver Modern",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": post
                },
                "shareMediaCategory": "ARTICLE",
                "media": [
                    {
                        "status": "READY",
                        "description": {
                            "text": message
                        },
                        "originalUrl": link,
                        "title": {
                            "text": link_text
                        }
                    }
                ]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "CONNECTIONS"
        }
    }
    print("dumps")
    return json.dumps(post_data)

def send_linkedin_post(filename, linkedin_post):
    # author = get_author
    print("hello from poster")

    api_url = 'https://api.linkedin.com/v2/ugcPosts'
    post_data = linkedin_post_data("author", linkedin_post)
    print(post_data)
    r = requests.post(api_url, headers=linkedin_headers, json=post_data)
    print("LinkedIn Post Response")
    print(r.json())









# Initializations
openai.api_key = appsecrets.OPEN_AI_API_KEY  

initialize_shopify_session()

linkedin_access_token = initialize_linkedin("linkedincredentials.json")
linkedin_headers = get_linkedin_headers(linkedin_access_token)

dbx = initialize_dropbox()       
tweepy_api = initialize_tweepy()

# Get our url argument from terminal
parser = argparse.ArgumentParser()
parser.add_argument("-url", "--parse_url", help="Youtube video to parse")
args = parser.parse_args()
youtube_url = args.parse_url

print("\n\n")
print("Let's make some money...")
print("\n\n")

#test code
send_linkedin_post("samplefile.txt", "linkedin post here")

# filename = save_to_mp3(youtube_url)
# transcriptname = mp3_to_transcript(filename)

#MAIN FUNCTION
if __name__ == '__main__':
    summary_ouput = 'outputs/summary_output.txt'
#utility
#     transcript_to_summary(transcriptname, filename)
#     source_to_content(filename, summary_ouput, 'prompts/visual.txt', "visual", empty_with_param)
# #done    
#     source_to_content(filename, transcriptname, 'prompts/blog.txt', "blog", send_shopify_article)
#     source_to_content(filename, summary_ouput, 'prompts/tweetstorm.txt', "TweetStorm", sendTweet)
#     source_to_content(filename, summary_ouput, 'prompts/email.txt', "Email", send_email_to_dropbox)
#     source_to_content(filename, summary_ouput, 'prompts/linkedin.txt', "LinkedIn", send_linkedin_post)
# #todo
#     source_to_content(filename, summary_ouput, 'prompts/script.txt', "youtubescript", empty_with_param)
#     source_to_content(filename, summary_ouput, 'prompts/story.txt', "story", empty_with_param)
# #to repurpose
#     source_to_content(filename, summary_ouput, 'prompts/stepguide.txt', "stepguide", empty_with_param)
#     source_to_content(filename, summary_ouput, 'prompts/takeaways.txt', "takeaways", empty_with_param)
#     source_to_content(filename, summary_ouput, 'prompts/quiz.txt', "quiz", empty_with_param)
    
    