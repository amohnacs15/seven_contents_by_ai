import sys
import os
sys.path.append("../src")

import requests
import appsecrets
from storage.firebase_storage import firebase_storage_instance, PostingPlatform
import json
import content.youtube_content_repo as youtube_content_repo

# Set your API endpoint URL and access token
upload_endpoint = "https://api.tiktok.com/open_api/v1.1/video/upload/"
auth_endpoint = "https://open-api.tiktok.com/oauth/access_token"

def get_authentication_headers():
    # Make a request to the API endpoint with the necessary parameters and authenticate
    response = requests.post(auth_endpoint, params={
        "app_id": appsecrets.TIK_TOK_APP_ID, 
        "app_secret": appsecrets.TIK_TOK_CLIENT_SECRET, 
        "grant_type": 'authorization_code'
    })

    # Get the access token from the response
    access_token = response.json()["access_token"]

    # Use the access token to make authenticated requests to the TikTok API
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers

def tiktok_video_upload( scheduled_datetime_str, post_params_json ):

    auth_headers = get_authentication_headers()

    # Open the video file and read its contents
    with open("video.mp4", "rb") as file:
        video_data = file.read()

    # Set the API parameters
    params = {
        # "access_token": access_token,
        "file_name": post_params_json['remote_video_url'],
        "file_size": len(video_data)
    }

    try:
        # Send a POST request to the API endpoint with the video file data and parameters
        response = requests.post(
            headers=auth_headers,
            url=upload_endpoint, 
            data=params, 
            files={"video": video_data}
        )
        response_data = json.loads(response.text)

        # Check for errors in the response
        if response_data.get("status_code") != 0:
            print(f"Error uploading video: {response_data.get('description')}")
        else:
            # Get the video ID from the response data
            video_id = response_data["video"]["vid"]
            print(f"Video uploaded successfully with ID: {video_id}")

    except Exception as e:
        print(f'error parsing json {e}')
        print(f'TIKTOK {post_params_json}')
        return 'error parsing json' 