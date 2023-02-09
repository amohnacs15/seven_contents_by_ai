#Image Creation and Downloads
import replicate
import appsecrets
import requests
import json

def get_unsplash_image_url( search_query ):
    url = 'https://api.unsplash.com/photos/random'
    params = {
        'query': search_query
    }
    headers = {
        'Accept-Version': "v1",
        'Authorization': 'Client-ID ' + appsecrets.UNSPLASH_ACCESS_KEY
    }
    response = requests.get( 
        url = url, 
        params = params,
        headers = headers
    )
    json_content = json.loads( response.content )
    return json_content['urls']['regular']


def get_ai_image(visual_prompt, width = 1024, height = 768):
    print('begin image processing')
    api = replicate.Client(appsecrets.REPLICATE_TOKEN)
    model = api.models.get("tstramer/midjourney-diffusion")
    version = model.versions.get("436b051ebd8f68d23e83d22de5e198e0995357afef113768c20f0b6fcef23c8b")

#     # https://replicate.com/tstramer/midjourney-diffusion/versions/436b051ebd8f68d23e83d22de5e198e0995357afef113768c20f0b6fcef23c8b#input
    inputs = {
#         # Input prompt
        'prompt': visual_prompt,

#         # Specify things to not see in the output # 'negative_prompt': ...,

#         # Width of output image. Maximum size is 1024x768 or 768x1024 because # of memory limits
        'width': width,

#         # Height of output image. Maximum size is 1024x768 or 768x1024 because of memory limits
        'height': height,

#         # Prompt strength when using init image. 1.0 corresponds to full destruction of information in init image
        'prompt_strength': 0.8,

#         # Number of images to output. # Range: 1 to 4
        'num_outputs': 1,

#         # Number of denoising steps # Range: 1 to 500
        'num_inference_steps': 50,

#         # Scale for classifier-free guidance # Range: 1 to 20
        'guidance_scale': 7.5,

#         # Choose a scheduler.
        'scheduler': "DPMSolverMultistep",

#         # Random seed. Leave blank to randomize the seed
#         # 'seed': ...,
    }

#     # https://replicate.com/tstramer/midjourney-diffusion/versions/436b051ebd8f68d23e83d22de5e198e0995357afef113768c20f0b6fcef23c8b#output-schema
    output = version.predict(**inputs)
    print("midjourney output")
    print(output[0])
    output[0]