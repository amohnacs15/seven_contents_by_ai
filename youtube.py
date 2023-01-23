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

import appsecrets

# Original 7 content functions

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

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

# Dropbox functions

def dropbox_connect():
    """Create a connection to Dropbox."""
    print("Initializing Dropbox API...") 
    try:
        dbx = dropbox.Dropbox(appsecrets.DROPBOX_APP_KEY)
        print('Dropbox initialized successfully')
    except AuthError as e:
        print('Error connecting to Dropbox with access token: ' + str(e))
    return dbx

def dropbox_upload_file(local_path, local_file, dropbox_file_path):
    """Upload a file from the local machine to a path in the Dropbox app directory.

    Args:
        local_path (str): The path to the local file.
        local_file (str): The name of the local file.
        dropbox_file_path (str): The path to the file in the Dropbox app directory.

    Example:
        dropbox_upload_file('.', 'test.csv', '/stuff/test.csv')

    Returns:
        meta: The Dropbox file metadata.
    """

    try:
        # dbx = dropbox_connect()
        local_file_path = pathlib.Path(local_path) / local_file

        with local_file_path.open("rb") as f:
            meta = dbx.files_upload(f.read(), dropbox_file_path, mode=dropbox.files.WriteMode("overwrite"))

            return meta
    except Exception as e:
        print('Error uploading file to Dropbox: ' + str(e))     

# Initializations
openai.api_key = appsecrets.OPEN_AI_API_KEY  
dbx = dropbox_connect()        

#YOUTUBE URL INSERT HERE   
youtube_url = "https://www.youtube.com/watch?v=5HdhvGkvk8c"
filename = save_to_mp3(youtube_url)
transcriptname = mp3_to_transcript(filename)

#MAIN FUNCTION
if __name__ == '__main__':
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
    
    #Blog Post
    feedin = open_file(transcriptname)
    text1 = open_file('prompts/blog.txt').replace('<<FEED>>', feedin)
    finaltext = gpt_3(text1)
    print('\n\n\n', 'Blog Post:\n\n', finaltext)
    save_file('outputs/blog_output.txt', finaltext)
    
    #Step-by-Step
    feedin10 = open_file('outputs/summary_output.txt')
    text20 = open_file('prompts/stepguide.txt').replace('<<FEED>>', feedin10)
    finaltext10 = gpt_3(text20)
    print('\n\n\n', 'Step-by-Step Guide:\n\n', finaltext10)
    save_file('outputs/stepguide_output.txt', finaltext10)
    
    #Social
    feedin1 = open_file('outputs/summary_output.txt')
    text2 = open_file('prompts/socialmedia.txt').replace('<<FEED>>', feedin1)
    finaltext1 = gpt_3(text2)
    print('\n\n\n', 'Social Media:\n\n', finaltext1)
    save_file('outputs/socialmedia_output.txt', finaltext1)
    
    #Visual
    feedin2 = open_file('outputs/summary_output.txt')
    text3 = open_file('prompts/visual.txt').replace('<<FEED>>', feedin2)
    finaltext2 = gpt_3(text3)
    print('\n\n\n', 'Visual:\n\n', finaltext2)
    save_file('outputs/visual_output.txt', finaltext2)
    
    #Takeaways
    feedin3 = open_file('outputs/summary_output.txt')
    text4 = open_file('prompts/takeaways.txt').replace('<<FEED>>', feedin3)
    finaltext3 = gpt_3(text4)
    print('\n\n\n', 'Takeaways:\n\n', finaltext3)
    save_file('outputs/takeaways_output.txt', finaltext3)
    
    #Short Video
    feedin4 = open_file('outputs/summary_output.txt')
    text5 = open_file('prompts/script.txt').replace('<<SUM>>', feedin4)
    finaltext4 = gpt_3(text5)
    print('\n\n\n', 'Youtube Script:\n\n', finaltext4)
    save_file('outputs/script_output.txt', finaltext4)
    
    #Story
    feedin5 = open_file('outputs/summary_output.txt')
    text6 = open_file('prompts/story.txt').replace('<<FEED>>', feedin5)
    finaltext5 = gpt_3(text6)
    print('\n\n\n', 'Story:\n\n', finaltext5)
    save_file('outputs/story_output.txt', finaltext5)
    
    #Quiz
    feedin6 = open_file('outputs/summary_output.txt')
    text7 = open_file('prompts/quiz.txt').replace('<<FEED>>', feedin6)
    finaltext6 = gpt_3(text7)
    print('\n\n\n', 'Quiz:\n\n', finaltext6)
    save_file('outputs/quiz_output.txt', finaltext6)
    
    