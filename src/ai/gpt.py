import sys
import os
sys.path.append("../src")

import whisper
import warnings
warnings.filterwarnings("ignore")
import openai
import textwrap
import utility.utils as utils
import appsecrets as appsecrets
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
    result = model.transcribe(sound, fp16=False, language = 'en')

    yttrans = (result['text'])
    result_path = mp3_filename + '_transcript.txt'
    utils.save_file(result_path, yttrans)
    print(f'saved mp3 transcript: {yttrans}')
    return result_path

def transcript_to_summary(transcriptname, filename):
    alltext = utils.open_file(transcriptname)
    chunks = textwrap.wrap(alltext, 2500)
    result = list()
    count = 0
    for chunk in chunks:
        count = count + 1
        file_path_input = os.path.join("src", "input_prompts", "summary.txt")
        prompt = utils.open_file(file_path_input).replace('<<SUMMARY>>', chunk)
        prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
        summary = gpt_3(prompt)
        print('\n\n\n', count, 'out of', len(chunks), 'Compressions', ' : ', summary)
        result.append(summary)
    file_path_output = os.path.join("src", "outputs", "summary_output.txt")    
    utils.save_file(file_path_output, '\n\n'.join(result))

def get_gpt_generated_text( prompt_source, polish_output ):
    # get the first draft of the generated text
    feedin_source_file = os.path.join("src", "outputs", "summary_output.txt")
    feed_source = utils.open_file(feedin_source_file)
    applied_prompt = utils.open_file(prompt_source).replace('<<FEED>>', feed_source)
    draft = gpt_3(applied_prompt)

    # get the second draft stripped of identifying material
    polish_source_file = os.path.join("src", "input_prompts", "polish.txt")
    polished_applied_prompt = utils.open_file(polish_source_file).replace('<<FEED>>', draft)
    return gpt_3(polished_applied_prompt)

def generate_prompt_response( 
        prompt_source, 
        image_query_term, 
        polish_post,
        post_num, 
        upload_func 
    ):
    """
    Convert a single file of language to another using chat GPT and upload to dropbox
        
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
    for num in range(post_num):
        print(f'Processing #{num} of {prompt_source}')
        gpt_text = get_gpt_generated_text(prompt_source, polish_post)
        upload_func(gpt_text, image_query_term)

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

def prompt_to_string_from_file( prompt_source_file, feedin_source_file ):
    feed_source = utils.open_file(feedin_source_file)
    appliedprompt = utils.open_file(prompt_source_file).replace('<<FEED>>', feed_source)
    finaltext = gpt_3(appliedprompt)
    return finaltext

def prompt_to_string( prompt_source_file, feedin_source ):
    appliedprompt = utils.open_file(prompt_source_file).replace('<<FEED>>', feedin_source)
    finaltext = gpt_3(appliedprompt)
    return finaltext