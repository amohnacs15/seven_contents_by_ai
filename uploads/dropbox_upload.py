#DROPBOX 
import dropbox
from dropbox.exceptions import AuthError
import pathlib
import appsecrets

def initialize_dropbox():
        """Create a connection to Dropbox."""
        try:
            dbx = dropbox.Dropbox(appsecrets.DROPBOX_APP_TOKEN)
            print('Dropbox Initialized Successfully')
        except AuthError as e:
            print('Error Connecting to Dropbox')
        return dbx

def dropbox_upload_file(dbx, local_path, local_file, dropbox_file_path):
    """Upload a file from the local machine to a path in the Dropbox app directory.

    Args:
        local_path (str): The path to the local file.
        local_file (str): The name of the local file.
        dropbox_file_path (str): The path to the file in the Dropbox app directory.

    Example:
        source_to_content(filename, transcriptname, 'prompts/blog.txt', "blog")

    Returns:
        meta: The Dropbox file metadata.
    """

    try:
        # dbx = dropbox_connect()
        local_file_path = pathlib.Path(local_path) / local_file

        with local_file_path.open("rb") as f:
            meta = dbx.files_upload(f.read(), dropbox_file_path, mode=dropbox.files.WriteMode("overwrite"))

            print("Upload success of " + local_file)

            return meta
    except Exception as e:
        print('Error uploading file to Dropbox: ' + str(e))          
