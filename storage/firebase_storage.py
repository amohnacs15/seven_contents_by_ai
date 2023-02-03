import pyrebase
import appsecrets

class FirebaseStorage():

    @classmethod
    def upload_mp3(self, remote_storage_path, local_path):
        firebase = pyrebase.initialize_app(appsecrets.firebase_config)
        firebase.storage().child(remote_storage_path).put("output_downloads/speech_to_text.mp3")

    def get_url(self, child_path_to_file):
        firebase = pyrebase.initialize_app(appsecrets.firebase_config)
        print(firebase.storage().child(child_path_to_file).get_url(None))
