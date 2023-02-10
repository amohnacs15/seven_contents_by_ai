import os
import datetime
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
import appsecrets
import google.oauth2.credentials
import google_auth_oauthlib.flow
import flask
import os
import pickle

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaFileUpload

# Build the YouTube API client
api_service_name = "youtube"
api_version = "v3"
CLIENT_SECRET_FILE = "client_secret_272470980608-16hgrujprvp3738vhakhc03f0naep0ti.apps.googleusercontent.com.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def upload_video_to_youtube ( upload_file_path ):
    # -*- coding: utf-8 -*-

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

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE, 
        SCOPES
    )
    credentials = flow.run_local_server()
    #this (points down) needs work so we can acutally access across sessions
    with open('token.pickle', 'wb') as token:
        pickle.dump(credentials, token)
    print('\nAuthentication complete. Uploading Video...\n')
    youtube = googleapiclient.discovery.build(
        api_service_name, 
        api_version, 
        credentials=credentials
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "My Video Title",
                "description": "This is a description of my video.",
                "tags": [
                    "tag1",
                    "tag2",
                    "tag3",
                ],
                "categoryId": 22,
            },
            "status": {
                "privacyStatus": "public",
                "embeddable": True,
                "license": "youtube",
                "publicStatsViewable": True
            }
        },
        media_body=MediaFileUpload(upload_file_path)
    )
    response = request.execute()

    print(response)
    return response

def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt    