import requests
import json
import appsecrets
import utility.utils as utils
import media.image_creator as image_creator
import storage.firebase_storage as firebase
import ai.speech_synthesis as speech_synthesis
import time

movies_url = 'https://api.json2video.com/v2/movies'

'''
Polls to get our movie response. Repeatedly pining off the server until we get the response we want.

@returns: remote movie url
'''
def get_edited_movie_url( uploaded_project_id ):
    # status states: not started, done, in progress
    video_upload_status='not started'

    params = dict()
    params['project'] = uploaded_project_id
    headers = dict()
    headers['x-api-key'] = appsecrets.JSON_TO_VIDEO_API_KEY

    while (video_upload_status != 'done'):
        response = requests.get( 
            url = movies_url, 
            params = params, 
            headers = headers 
        )
        video_upload_status = get_response_status_check(response)
        if (video_upload_status == 'error'):
            return "no movie url"
        time.sleep(25)

    movie_url = get_response_movie_url(response)
    return movie_url

'''
Send the request to get create our movie programmatically.

WARNING: This influences our quota

We pull the data from files.  To create our video scenes.
Then we poll the get request until the video is ready, giving us the url.

@returns: remote URL for our video
'''
def edit_movie_for_remote_url():
    post_headers = {
        'x-api-key': appsecrets.JSON_TO_VIDEO_API_KEY
    }

    # preparing the pieces
    scene_images = get_scene_images_array()
    story_text = utils.open_file('outputs/story_output.txt')
    speech_bundle = speech_synthesis.text_to_speech(story_text)
    # speech_bundle = {'speech_duration': 96.8125, 'speech_remote_path': 'ai_content_machine/speech_to_text.mp3'}
    print(speech_bundle)
    video_json = create_video_json(
        image_array = scene_images, 
        mp3_duration = speech_bundle['speech_duration'],
        mp3_remote_path = speech_bundle['speech_remote_path']
    )
    # making the actual request
    response = requests.post(
        url = movies_url, 
        json = video_json, 
        headers = post_headers
    )
    project_id = post_response_project_id(response)

    print('\n project id \n')
    print(project_id)

    movie_url = get_edited_movie_url(project_id)
    return movie_url

#--------------- Preparing The Pieces -----------------------------------------------------    
'''
Generates our AI images for the video we are creating.

WARNING: This procedure costs money.  Use a dummy list where possible.

@returns: array of image urls
'''
def get_scene_images_array():
    images = []

    promptfile = open('output_story_scenes/mjv4_output.txt', 'r')
    prompts = promptfile.readlines()

    for prompt in prompts:
        image = image_creator.get_unsplash_image_url(prompt)
        images.append(image)

    return images    

'''
Dynamically generates our movie json for generation using supplied arguments.
Transitions, inclusions of audio, and quality are hard-coded.

@returns: json formatted string
'''
def create_video_json( image_array, mp3_duration, mp3_remote_path ):
    scene_duration = mp3_duration / len(image_array)
    mp3_ref_url = firebase.get_url(mp3_remote_path)

    scene_comments = get_scene_comment_array()

    video_params = {
        "resolution": "full-hd",
        "quality": "high",
        "elements": [
            {
                "type": "audio",
                "src": mp3_ref_url,
                "volume": 0.8,
                "duration": -2,
                "fade-out": 2
            }
        ],
        "scenes": []
    }

    for index in range(len(image_array)):
        video_params['scenes'].append(
        {
            'comment': scene_comments[index],
            "transition": {
                "style": "fade",
                "duration": 1.5
            },
            "elements": [
                {
                    "type": "image",
                    "src": image_array[index],
                    "duration": scene_duration
                }
            ] 
        }
    )

    return video_params

'''
Simply reads from our file system to get the description of scenes created by ChatGPT

@returns: array of strings
'''
def get_scene_comment_array():
    pathfolder = "output_story_scenes"
    return [
        utils.open_file(f'{pathfolder}/scene1.txt'),
        utils.open_file(f'{pathfolder}/scene2.txt'),
        utils.open_file(f'{pathfolder}/scene3.txt'),
        utils.open_file(f'{pathfolder}/scene4.txt'),
        utils.open_file(f'{pathfolder}/scene5.txt'),
        utils.open_file(f'{pathfolder}/scene6.txt'),
        utils.open_file(f'{pathfolder}/scene7.txt'),
        utils.open_file(f'{pathfolder}/scene8.txt'),
        utils.open_file(f'{pathfolder}/scene9.txt'),
        utils.open_file(f'{pathfolder}/scene10.txt')
    ]


#--------------- Display Status -----------------------------------------------------------
'''
Extracts the response status assuming a success response

@returns: status string
'''
def get_response_status_check( data ):
    response = dict()
    response['json_data'] = json.loads( data.content ) # response data from the api
    response['json_data_pretty'] = json.dumps( response['json_data'], indent = 4 ) # pretty print for cli

    print(response['json_data_pretty'])

    status = response['json_data']['movie']['status']

    print("Pinging Status...")
    print(status)
    
    return status

'''
Extracts the response url assuming a success response

@returns: remote url for our created video
'''
def get_response_movie_url( data ) :
    response = dict()
    response['json_data'] = json.loads( data.content ) # response data from the api
    response['json_data_pretty'] = json.dumps( response['json_data'], indent = 4 ) # pretty print for cli

    movie_url = response['json_data']['movie']['url']

    print("\nMovie url...\n")
    print(movie_url)
    
    return movie_url

'''
Extracts the response status assuming a success response

@returns: project id string
'''
def post_response_project_id( data ) :
    response = dict()
    response['json_data'] = json.loads( data.content ) # response data from the api
    response['json_data_pretty'] = json.dumps( response['json_data'], indent = 4 ) # pretty print for cli

    print(response['json_data_pretty'])

    response['success'] = response['json_data']['success']
    response['project_id'] = response['json_data']['project']
    response['timestamp'] = response['json_data']['timestamp']

    if (response['success'] == True):
        return response['project_id']
    else:
        return -1    

# --------------- Dummy Code -----------------------------

example_of_running_movie_generation = {
    "success": "true",
    "movie": {
        "success": 'false',
        "status": "running",
        "message": "downloading assets",
        "project": "pQNF8AablTeqEMWb",
        "url": 'null',
        "created_at": "2023-02-08T10:52:57.636Z",
        "ended_at": 'null',
        "draft": 'false',
        "rendering_time": 'null'
    },
    "remaining_quota": {
        "movies": 14,
        "drafts": 37
    }
}

example_video = {
    "resolution": "full-hd",
    "quality": "high",
    "scenes": [
        {
            "comment": "Scene #1",
            "transition": {
                "style": "circleopen",
                "duration": 1.5
            },
            "elements": [
                {
                    "type": "image",
                    "src": "https://assets.json2video.com/assets/images/london-01.jpg",
                    "duration": 10
                }, 
                {
                    "type": "audio",
                    "src": "https://assets.json2video.com/assets/audios/thunder-01.mp3"
                }
            ]
        },
        {
            "comment": "Scene #2",
            "transition": {
                "style": "wipeup",
                "duration": 1.5
            },
            "elements": [
                {
                    "type": "image",
                    "src": "https://assets.json2video.com/assets/images/london-02.jpg",
                    "duration": 10
                }
            ]
        },
        {
            "comment": "Scene #3",
            "transition": {
                "style": "fade",
                "duration": 1.5
            },
            "elements": [
                {
                    "type": "image",
                    "src": "https://assets.json2video.com/assets/images/london-03.jpg",
                    "duration": 10
                }
            ]
        }
    ]
}    

debug_image_array = [
    'https://replicate.delivery/pbxt/CAacYFtCHTYGBhexflfELSivW5AkDZkdlfzaorDeoL3SfHIHE/out-0.png',
    'https://replicate.delivery/pbxt/CxPhtmKZdeXes0rPNZP8l4vKxXQXDcRjOGmPOLbYXUOXggcQA/out-0.png',
    'https://replicate.delivery/pbxt/lcfdiBzud0UGZ6tYjchdwr8tlhCqbwwuUeWQiMAzqvV0ggcQA/out-0.png',
    'https://replicate.delivery/pbxt/gvEuhgjhQRpQNh5vD3jjtQyD6z45PerHcUpy52unfHaRhgcQA/out-0.png',
    'https://replicate.delivery/pbxt/NdUh5g8r9rL6L5ZxzkXM3fSf9WyH8MHKCb21qLMtnnfbDB5gA/out-0.png',
    'https://replicate.delivery/pbxt/bTfgKIDN5Q3wLadorLxJyeMijr1xFP29F29CuhurEnFKigcQA/out-0.png',
    'https://replicate.delivery/pbxt/KpnnkNtrBFYeekxloJ7kp3UK2VbTFIzCH9H0uG9Is0UsigcQA/out-0.png',
    'https://replicate.delivery/pbxt/pprpxUggo7qqLNqhgfJMeMjSXRjXeXgjRJjsovhqIDURGB5gA/out-0.png',
    'https://replicate.delivery/pbxt/5G2cHubkk05fDKZbesjqffhXjTecbTPgq0Y96A0NdCczcEkDC/out-0.png',
    'https://replicate.delivery/pbxt/MJyUXTEyGIauERB6KBpnOgBrjpeqcLrsAJQTrnmZW2ZBSQOIA/out-0.png'
]