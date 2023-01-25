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

import appsecrets







#Initializations
def initialize_tweepy():
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(appsecrets.TWITTER_API_KEY, appsecrets.TWITTER_API_SECRET)
    auth.set_access_token(appsecrets.TWITTER_API_AUTH_TOKEN, appsecrets.TWITTER_API_AUTH_SECRET)

    return tweepy.API(auth)

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
    dropbox_upload_file('outputs', 'summary_output.txt', '/' + filename.replace(".mp3", "") + '/' + 'summary_output.txt')

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







def dropbox_connect():
        """Create a connection to Dropbox."""
        print("Initializing Dropbox API...") 
        try:
            dbx = dropbox.Dropbox(appsecrets.DROPBOX_APP_TOKEN)
            print('*****Dropbox initialized successfully')
        except AuthError as e:
            print('*****Error connecting to Dropbox')
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

            print("*****upload success of " + local_file)

            return meta
    except Exception as e:
        print('*****Error uploading file to Dropbox: ' + str(e))          

# Twitter Upload
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







# Initializations
openai.api_key = appsecrets.OPEN_AI_API_KEY  

dbx = dropbox_connect()       
tweepy_api = initialize_tweepy()
try:
    tweepy_api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during Tweepy authentication") 

#YOUTUBE URL PROMPT HERE   
youtube_url = input("\n\n\nPlease enter your Youtube URL to generate content from:")
print("Let's get started...")
print("\n\n\n")
filename = save_to_mp3(youtube_url)
transcriptname = mp3_to_transcript(filename)

#MAIN FUNCTION
if __name__ == '__main__':
    transcript_to_summary(transcriptname, filename)
    
    source_to_content(filename, transcriptname, 'prompts/blog.txt', "blog", emptyWithParam)
    source_to_content(filename, 'outputs/summary_output.txt', 'prompts/stepguide.txt', "stepguide", emptyWithParam)
    source_to_content(filename, 'outputs/summary_output.txt', 'prompts/linkedin.txt', "LinkedIn", emptyWithParam)
    source_to_content(filename, 'outputs/summary_output.txt', 'prompts/tweetstorm.txt', "TweetStorm", sendTweet)
    source_to_content(filename, 'outputs/summary_output.txt', 'prompts/email.txt', "Email", emptyWithParam)
    source_to_content(filename, 'outputs/summary_output.txt', 'prompts/visual.txt', "visual", emptyWithParam)
    source_to_content(filename, 'outputs/summary_output.txt', 'prompts/takeaways.txt', "takeaways", emptyWithParam)
    source_to_content(filename, 'outputs/summary_output.txt', 'prompts/script.txt', "youtubescript", emptyWithParam)
    source_to_content(filename, 'outputs/summary_output.txt', 'prompts/story.txt', "story", emptyWithParam)
    source_to_content(filename, 'outputs/summary_output.txt', 'prompts/quiz.txt', "quiz", emptyWithParam)
    
    