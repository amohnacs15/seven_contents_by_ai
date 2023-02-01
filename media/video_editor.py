import requests
import json
import appsecrets

def getEditedMovie():
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

    print('Get Success? ')
    displayGetCallData(response)

def sendMovieForEditing():
    post_url = 'https://api.json2video.com/v2/movies'
    post_headers = {
        'x-api-key': appsecrets.JSON_TO_VIDEO_API_KEY
    }

    response = requests.post(
        url = post_url, 
        params = debug_video, 
        headers = post_headers
    )
    displayPostCallData(response)
    return response['success']

def displayGetCallData( data ) :
    response = dict()
    response['json_data'] = json.loads( data.content ) # response data from the api
    response['json_data_pretty'] = json.dumps( response['json_data'], indent = 4 ) # pretty print for cli

    print ("\nSuccess? ") # title
    print(response['movies'][0]['url'])

def displayPostCallData( data ) :
    response = dict()
    response['json_data'] = json.loads( data.content ) # response data from the api
    response['json_data_pretty'] = json.dumps( response['json_data'], indent = 4 ) # pretty print for cli

    print ("\nSuccess? ") # title
    print (response['success'])   
    print(response['url'])

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

uploaded_project_id = ''