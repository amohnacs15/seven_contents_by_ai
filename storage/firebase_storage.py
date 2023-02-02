import pyrebase
import appsecrets

class FirebaseStorage():

    storage = None

    def __init__(self):
        
        firebase = pyrebase.initialize_app(appsecrets.firebase_config)
        storage = firebase.storage()

    @classmethod
    def upload_mp3(self, remote_storage_path, local_path):
        self.storage.child(remote_storage_path).put("output_downloads/speech_to_text.mp3")


