import requests
import json
import appsecrets
import utility.utils as utils
import media.image_creator as image_creator
import storage.firebase_storage as firebase
import ai.speech_synthesis as speech_synthesis

def get_edited_movie():
    get_url = 'https://api.json2video.com/v2/movies?'

    params = dict()
    params['project'] = uploaded_project_id
    headers = dict()
    headers['x-api-key'] = appsecrets.JSON_TO_VIDEO_API_KEY

    response = requests.get( 
        url = get_url, 
        json = params, 
        headers = headers 
    )

    get_response_movie_url(response)

def send_movie_for_editing():
    post_url = 'https://api.json2video.com/v2/movies'
    post_headers = {
        'x-api-key': appsecrets.JSON_TO_VIDEO_API_KEY
    }

    scene_images = get_scene_images_array()
    story_text = utils.open_file('outputs/Story_Output.txt')
    speech_bundle = speech_synthesis.text_to_speech(story_text)
    video_json = create_video_json(
        image_array = scene_images, 
        mp3_duration = speech_bundle['speech_duration'],
        mp3_remote_path = speech_bundle['speech_remote_path']
    )

    response = requests.post(
        url = post_url, 
        json = video_json, 
        headers = post_headers
    )
    get_response_project_id(response)
    return response['success']

#--------------- Preparing The Pieces -----------------------------------------------------    

def get_scene_images_array():
    images = []

    promptfile = open('output_story_scenes/mjv4_output.txt', 'r')
    prompts = promptfile.readlines()

    for prompt in prompts:
        image = image_creator.get_ai_image(prompt)
        images.append(image)

    return images    

def create_video_json( image_array, mp3_duration, mp3_remote_path ):
    scene_duration = mp3_duration / len(image_array)
    mp3_ref_url = firebase.get_url(mp3_remote_path)

    scene_comments = get_scene_comment_array()

    video_params = {
        "resolution": "full-hd",
        "quality": "high",
        "elements": {
            "type": "audio",
            "src": mp3_ref_url,
            "volume": 0.8,
            "duration": -2,
            "fade-out": 2
        },
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
def get_response_movie_url( data ) :
    response = dict()
    response['json_data'] = json.loads( data.content ) # response data from the api
    response['json_data_pretty'] = json.dumps( response['json_data'], indent = 4 ) # pretty print for cli

    print ("\nSuccess? ") # title
    print(response['movies'][0]['url'])

def get_response_project_id( data ) :
    response = dict()
    response['json_data'] = json.loads( data.content ) # response data from the api
    response['json_data_pretty'] = json.dumps( response['json_data'], indent = 4 ) # pretty print for cli

    response['success'] = response['json_data']['success']
    response['project_id'] = response['json_data']['project']
    response['timestamp'] = response['json_data']['timestamp']

    print ("\nSuccess? ") # title
    print (response['success'])  
    if (response['success'] == True):
        return response['project_id']
    else:
        return -1    

# ---------------Getting completed video -----------------------------

debug_video = {
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