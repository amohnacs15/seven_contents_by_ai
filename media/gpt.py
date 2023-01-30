# Original 7 content functions
#GPT-3 Function        
import utility.utils as utils
import openai
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

import appsecrets

openai.api_key = appsecrets.OPEN_AI_API_KEY  

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
        'outtmpl': 'output_downloads/%(title)s-%(id)s.%(ext)s',
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
    result_path = mp3_filename + '_transcript.txt'
    utils.save_file(result_path, yttrans)
    return result_path

def transcript_to_summary(transcriptname, filename):
    alltext = utils.open_file(transcriptname)
    chunks = textwrap.wrap(alltext, 2500)
    result = list()
    count = 0
    for chunk in chunks:
        count = count + 1
        prompt = utils.open_file('prompts_input/summary.txt').replace('<<SUMMARY>>', chunk)
        prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
        summary = gpt_3(prompt)
        print('\n\n\n', count, 'out of', len(chunks), 'Compressions', ' : ', summary)
        result.append(summary)
    utils.save_file('outputs/summary_output.txt', '\n\n'.join(result))

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
        feedin = utils.open_file(feedin_source)
        appliedprompt = utils.open_file(prompt_source).replace('<<FEED>>', feedin)
        finaltext = gpt_3(appliedprompt)
        
        print('\n\n\n', type + ' post:\n\n', finaltext)

        saveFilePath = 'outputs/'+type+'_Output.txt'

        utils.save_file(saveFilePath, finaltext)
        upload_func(saveFilePath, finaltext)
        # dropbox_upload_file(saveFilePath, '/' + filename.replace(".mp3", "") + '/' + type + '_output.txt')
        # remove_file(saveFilePath)


