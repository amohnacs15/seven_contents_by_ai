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

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)
        

openai.api_key = open_file('openaiapikey.txt')      
        
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

#YOUTUBE URL INSERT HERE   
youtube_url = "https://www.youtube.com/watch?v=0juvbDj4Xns"
filename = save_to_mp3(youtube_url)

#Pathfolder
desktop_path = "/Users/adrian.mohnacs/Python/YTcontent/"
# two parameters if we already have an mp3
# folder_name = "YTcontent"
# file_name = 'ytyt.mp3'
file_path = os.path.join(desktop_path, filename)

# sound = file_path 
sound = filename
model = whisper.load_model("medium")
result = model.transcribe(sound, fp16=False)
yttrans = (result['text'])
print(yttrans)
save_file('youtubetext.txt', yttrans)

#MAIN FUNCTION
if __name__ == '__main__':
    alltext = open_file('youtubetext.txt')
    chunks = textwrap.wrap(alltext, 2500)
    result = list()
    count = 0
    for chunk in chunks:
        count = count + 1
        prompt = open_file('prompt.txt').replace('<<SUMMARY>>', chunk)
        prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
        summary = gpt_3(prompt)
        print('\n\n\n', count, 'out of', len(chunks), 'Compressions', ' : ', summary)
        result.append(summary)
    save_file('output.txt', '\n\n'.join(result))
    
    #Blog Post
    feedin = open_file('youtubetext.txt')
    text1 = open_file('prompt22.txt').replace('<<FEED>>', feedin)
    finaltext = gpt_3(text1)
    print('\n\n\n', 'Blog Post:\n\n', finaltext)
    save_file('bp.txt', finaltext)
    
    #Step-by-Step
    feedin10 = open_file('output.txt')
    text20 = open_file('prompt2.txt').replace('<<FEED>>', feedin10)
    finaltext10 = gpt_3(text20)
    print('\n\n\n', 'Step-by-Step Guide:\n\n', finaltext10)
    save_file('steps.txt', finaltext10)
    
    #Social
    feedin1 = open_file('output.txt')
    text2 = open_file('prompt3.txt').replace('<<FEED>>', feedin1)
    finaltext1 = gpt_3(text2)
    print('\n\n\n', 'Social Media:\n\n', finaltext1)
    save_file('some.txt', finaltext1)
    
    #Visual
    feedin2 = open_file('output.txt')
    text3 = open_file('prompt4.txt').replace('<<FEED>>', feedin2)
    finaltext2 = gpt_3(text3)
    print('\n\n\n', 'Visual:\n\n', finaltext2)
    save_file('Visual.txt', finaltext2)
    
    #Summary
    feedin3 = open_file('output.txt')
    text4 = open_file('prompt5.txt').replace('<<FEED>>', feedin3)
    finaltext3 = gpt_3(text4)
    print('\n\n\n', 'Summary:\n\n', finaltext3)
    save_file('Summary.txt', finaltext3)
    
    #Short Video
    feedin4 = open_file('Summary.txt')
    text5 = open_file('prompt6.txt').replace('<<SUM>>', feedin4)
    finaltext4 = gpt_3(text5)
    print('\n\n\n', 'Shorts:\n\n', finaltext4)
    save_file('Shorts.txt', finaltext4)
    
    #Story
    feedin5 = open_file('output.txt')
    text6 = open_file('prompt7.txt').replace('<<FEED>>', feedin5)
    finaltext5 = gpt_3(text6)
    print('\n\n\n', 'Story:\n\n', finaltext5)
    save_file('Story.txt', finaltext5)
    
    #Quiz
    feedin6 = open_file('output.txt')
    text7 = open_file('prompt8.txt').replace('<<FEED>>', feedin6)
    finaltext6 = gpt_3(text7)
    print('\n\n\n', 'Quiz:\n\n', finaltext6)
    save_file('Quiz.txt', finaltext6)
    
    