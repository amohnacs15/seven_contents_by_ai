# Original 7 content functions
#GPT-3 Function        
import utility.utils as utils
import whisper
import warnings
warnings.filterwarnings("ignore")
import openai
from time import time,sleep
import textwrap
import pandas as pd
import utility.utils as utils
import appsecrets
import content_creator
import storage.dropbox_uploader as dropbox_uploader

openai.api_key = appsecrets.OPEN_AI_API_KEY  

'''GPT #

    Args:
        string: Prompt for GPT processing

    Returns:
        String of AI generated content
'''
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
        prompt = utils.open_file('input_prompts/summary.txt').replace('<<SUMMARY>>', chunk)
        prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
        summary = gpt_3(prompt)
        print('\n\n\n', count, 'out of', len(chunks), 'Compressions', ' : ', summary)
        result.append(summary)
    utils.save_file('outputs/summary_output.txt', '\n\n'.join(result))

"""Convert a single file of language to another using chat GPT and upload to dropbox
        
    Args:
        feedin_source (str): The path to the file.
        prompt_source (str): The path for the GPT prompt.
        type (str): simple categorization to help with naming
        dropbox_file_path (str): The path to the file in the Dropbox app directory.

    Example:
        dropbox_upload_file('.', 'test.csv', '/stuff/test.csv')

    Returns: 
        Nothing
"""
def prompt_to_file( feedin_source_file, prompt_source, type, upload_func ):
    feed_source = utils.open_file(feedin_source_file)
    appliedprompt = utils.open_file(prompt_source).replace('<<FEED>>', feed_source)
    finaltext = gpt_3(appliedprompt)
        
    print('\n\n\n', type + ' post:\n\n', finaltext)

    saveFilePath = 'outputs/'+type+'_output.txt'

    utils.save_file(saveFilePath, finaltext)
    upload_func(caption = finaltext)

def prompt_to_file_upload( filename, feedin_source_file, prompt_source, type ):
    dbx = content_creator.dbx

    feed_source = utils.open_file(feedin_source_file)
    appliedprompt = utils.open_file(prompt_source).replace('<<FEED>>', feed_source)
    finaltext = gpt_3(appliedprompt)
        
    print('\n\n\n', type + ' post:\n\n', finaltext)

    file_local_path = 'outputs/' + type + '_output.txt'

    print('calling into dropbox')
    print('file_local_path: ' + file_local_path)
    print('dropbox destination path: ' + '/' + filename.replace(".mp3", "").replace("/output_downloads", "") + '/' + type + '_output.txt')

    utils.save_file(file_local_path, finaltext)
    dropbox_uploader.dropbox_upload_file(
        dropbox_instance = dbx,
        local_file_path = file_local_path,
        dropbox_file_path = '/' + filename.replace(".mp3", "").replace("/output_downloads", "") + '/' + type + '_output.txt'
    )
    utils.remove_file(file_local_path)        

def prompt_to_string( prompt_source, feedin_source_file ):
    feed_source = utils.open_file(feedin_source_file)
    appliedprompt = utils.open_file(prompt_source).replace('<<FEED>>', feed_source)
    finaltext = gpt_3(appliedprompt)
    return finaltext

