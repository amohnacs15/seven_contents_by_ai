import firebase_admin
from firebase_admin import credentials, initialize_app, storage

class FirebaseStorage():

    def __init__(self):
        # Fetch the service account key JSON file contents
        cred = credentials.Certificate('ai-content-machine-firebase-adminsdk-6zj7h-52e83f9aa9.json')
        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(cred, {
            'storage_bucket': 'ai-content-machine.appspot.com'
        })

        ref = storage.reference('/database')
        print(ref.get())

    @classmethod
    def upload_mp3(self, filepath):
        # 'bucket' is an object defined in the google-cloud-storage Python library.
        # See https://googlecloudplatform.github.io/google-cloud-python/latest/storage/buckets.html
        # for more details.
        bucket = storage.bucket("my first bucket")
        blob = bucket.blob(filepath)
        blob.upload_from_filename(filepath)

        # Opt : if you want to make public access from the URL
        # blob.make_public()

        print("your file url", blob.public_url)


