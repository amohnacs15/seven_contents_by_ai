import pyrebase
import appsecrets

def upload_mp3( remote_storage_path, local_path ):
    firebase = pyrebase.initialize_app(appsecrets.firebase_config)
    firebase.storage().child(remote_storage_path).put(local_path)
    print('successful firebase upload')

def get_url( child_path_to_file ):
    firebase = pyrebase.initialize_app(appsecrets.firebase_config)
    url = firebase.storage().child(child_path_to_file).get_url(None)
    return url

