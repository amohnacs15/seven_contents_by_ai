import openai
from time import time,sleep
import src.utility.utils as utils
import appsecrets

openai.api_key = appsecrets.OPEN_AI_API_KEY

def create_story_and_scenes( filename, story ):

    # turn story into scenes
    storyscene = utils.open_file('input_prompts/scenes.txt').replace('<<STORY>>', story)
    gpt_story_scene = gpt3_story_scene(storyscene)
    
    # Save each scene in its own file
    pathfolder = "output_story_scenes"
    utils.save_file(pathfolder + '/storyscene.txt', gpt_story_scene)
    split_story_into_scenes(pathfolder)

    scenes = [utils.open_file(f'{pathfolder}/scene1.txt'),
              utils.open_file(f'{pathfolder}/scene2.txt'),
              utils.open_file(f'{pathfolder}/scene3.txt'),
              utils.open_file(f'{pathfolder}/scene4.txt'),
              utils.open_file(f'{pathfolder}/scene5.txt'),
              utils.open_file(f'{pathfolder}/scene6.txt'),
              utils.open_file(f'{pathfolder}/scene7.txt'),
              utils.open_file(f'{pathfolder}/scene8.txt'),
              utils.open_file(f'{pathfolder}/scene9.txt'),
              utils.open_file(f'{pathfolder}/scene10.txt')]
    
    # Turn our scenes into AI prompts
    count = 0
    filename = "/mjv4_output.txt"
    utils.save_file(pathfolder + filename, '')
    for scene in scenes:
        count += 1    
        mjv4 = utils.open_file('input_prompts/mjv4prompts.txt').replace('<<SCENE>>', scene)
        desc = gpt3_story_scene(mjv4)

        print(desc)

        # and write to the same file
        current_file = open(pathfolder + filename, 'a')
        current_file.write('\n' + desc)
        current_file.close()

        if count > 10:
            return pathfolder+filename

def split_story_into_scenes(folder_path):
  # Open the story file
  with open(f"{folder_path}/storyscene.txt", "r", encoding='UTF-8') as story_file:
    # Read the entire file into a single string
    story = story_file.read()

  # Split the story into a list of scenes, using the word "Scene" as the delimiter
  scenes = story.split("Scene")

  # Iterate over the list of scenes
  for i, scene in enumerate(scenes):
    # Write each scene to a separate file
    if (i > 0):
        with open(f"{folder_path}/scene{i}.txt", "w", encoding='UTF-8') as scene_file:
            scene_file.write(scene)
        
def gpt3_story_scene(
    prompt, 
    engine='text-davinci-003', 
    temp=0.7, 
    top_p=1.0, 
    tokens=2000, 
    freq_pen=0.0, 
    pres_pen=0.0, 
    stop=['asdfasdf', 'asdasdf']
):
    max_retry = 5
    retry = 0
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()

    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
                
            text = response['choices'][0]['text'].strip()
            #text = re.sub('\s+', ' ', text)
            filename = '%s_gpt3.txt' % time()
            # utils.save_file('logger/%s' % filename, prompt + '\n\n==========\n\n' + text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)
