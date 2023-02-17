import sys
sys.path.append("../src")

import dropbox
from dropbox.exceptions import AuthError
import appsecrets 

"""Create a connection to Dropbox."""
def initialize_dropbox():
        try:
            dbx = dropbox.Dropbox(appsecrets.DROPBOX_APP_TOKEN)
            print('Dropbox Initialized Successfully')
        except AuthError as e:
            print('Error Connecting to Dropbox')
        return dbx

"""Upload a file from the local machine to a path in the Dropbox app directory.

    Args:
        local_path (str): The path to the local file.
        local_file (str): The name of the local file.
        dropbox_file_path (str): The path to the file in the Dropbox app directory.

    Example:
        source_to_content(filename, transcriptname, 'prompts_input/blog.txt', "blog")

    Returns:
        meta: The Dropbox file metadata.
"""
def dropbox_upload_file( dropbox_instance, local_file_path, dropbox_file_path ):
    try:
        local_file_path = 'outputs/linkedin_output.txt'
        with local_file_path.open("rb") as f:
            print(local_file_path)
            meta = dropbox_instance.files_upload(
                f.read(), 
                dropbox_file_path, 
                mode=dropbox.files.WriteMode("overwrite")
            )

            print("Upload success to DBX")

            return meta
    except Exception as e:
        print('Error uploading file to Dropbox: ' + str(e))          

def prepareFileForDropboxUpload( filename, input ):   
    first_word = input.split()[0]
    dropbox_location = '/' + filename.replace(".mp3", "") + '/' + first_word + '.txt'
    # dbx.drop_upload_file( dbx, filename, dropbox_location)