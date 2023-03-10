import sys
import os
sys.path.append("../src")

import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
import ai.gpt as gpt3
from storage.firebase_storage import firebase_storage_instance, PostingPlatform
import media.video_downloader as video_downloader
import utility.time_utils as time_utils
import pickle
import json

# Build the YouTube API client
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

CLIENT_SECRET_FILE = "client_secret_272470980608-16hgrujprvp3738vhakhc03f0naep0ti.apps.googleusercontent.com.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def schedule_youtube_video ( remote_video_url ):  
    summary = os.path.join('src', 'outputs', 'summary_output.txt')
    title = gpt3.prompt_to_string(
        os.path.join('src', 'input_prompts', 'youtube_title.txt'),
        feedin_source_file=summary
    )
    title = title.replace('"', '')
    description = gpt3.prompt_to_string(
        prompt_source=os.path.join('src', 'input_prompts', 'youtube_description.txt'),
        feedin_source_file=summary
    )

    payload = dict()
    payload['title'] = title
    payload['description'] = description
    payload['remote_video_url'] = remote_video_url

    result = firebase_storage_instance.upload_scheduled_post(
        PostingPlatform.YOUTUBE,
        payload
    )
    return result

def get_youtube_credentials():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Get credentials and create an API client
    # Get the path to the parent directory
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    file_path = os.path.join(parent_dir, CLIENT_SECRET_FILE)
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        file_path, 
        SCOPES
    )

    # get cached values
    token_file = os.path.join('src', 'yt_access_token.pickle')
    with open(token_file, "rb") as input_file:
        credentials = pickle.load(input_file)

    if (credentials == ''):
        credentials = flow.run_local_server()
        
        with open(token_file, 'wb') as token:
            pickle.dump(credentials, token)
                    
    print('\nYoutube authentication complete\n')
    return credentials


def post_upload_video_to_youtube():
    '''
    # Sample Python code for youtube.videos.insert
    # NOTES:
    # 1. This sample code uploads a file and can't be executed via this interface.
    #    To test this code, you must run it locally using your own API credentials.
    #    See: https://developers.google.com/explorer-help/code-samples#python
    # 2. This example makes a simple upload request. We recommend that you consider
    #    using resumable uploads instead, particularly if you are transferring large
    #    files or there's a high likelihood of a network interruption or other
    #    transmission failure. To learn more about resumable uploads, see:
    #    https://developers.google.com/api-client-library/python/guide/media_upload

    '''
    earliest_scheduled_datetime_str = firebase_storage_instance.get_earliest_scheduled_datetime(PostingPlatform.YOUTUBE)
    if (earliest_scheduled_datetime_str == ''): return 'no posts scheduled'
    print(f'YT last posted time: {earliest_scheduled_datetime_str}')
    
    ready_to_post = time_utils.is_current_posting_time_within_window(earliest_scheduled_datetime_str)
    if (ready_to_post):   
        post_params_json = firebase_storage_instance.get_specific_post(
            PostingPlatform.YOUTUBE, 
            earliest_scheduled_datetime_str
        )
        try:
            post_params = json.loads(post_params_json)
            if (post_params['remote_video_url'] == 'no movie url'):
                firebase_storage_instance.delete_post(
                    PostingPlatform.YOUTUBE,
                    earliest_scheduled_datetime_str
                )
                post_upload_video_to_youtube()

            print('\nYOUTUBE post_params: ', post_params, '\n')
        except:
            print('YOUTUBE error parsing post params')
            print('post_params_json: ', post_params_json)
            return 'Error parsing post params'

        try:
            upload_file_path = video_downloader.download_video(
                post_params['remote_video_url']
            )
        except Exception as e:
            print(f'Error downloading video: {e}')
            return
    
        youtube = googleapiclient.discovery.build(
            API_SERVICE_NAME, 
            API_VERSION, 
            credentials = get_youtube_credentials()
        )

        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": post_params['title'],
                    "description": post_params['description']
                },
                "status": {
                    "privacyStatus": "private",
                    "embeddable": True,
                    "license": "youtube",
                    "publicStatsViewable": True
                }
            },
            media_body=MediaFileUpload(upload_file_path)
        )
        try:
            response = request.execute()
            firebase_storage_instance.delete_post(
                PostingPlatform.YOUTUBE, 
                earliest_scheduled_datetime_str
            )
        except Exception as e:    
            response = e
        return response
