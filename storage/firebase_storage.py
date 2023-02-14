import pyrebase
import appsecrets
from enum import Enum
import json
import utility.scheduler as scheduler
import datetime

class PostingPlatform(Enum):
        FACEBOOK = 'facebook'
        INSTAGRAM = 'instagram'
        TWITTER = 'twitter'
        YOUTUBE = 'youtube'
        SHOPIFY = 'shopify'

class FirebaseStorage():
    # Constants
    POSTS_COLLECTION = "posts"

    # Initializations    
    firebase = pyrebase.initialize_app(appsecrets.firebase_config)
    firestore = firebase.database()
    storage = firebase.storage()

    @classmethod
    def upload_mp3( self, remote_storage_path, local_path ):
        self.storage.child(remote_storage_path).put(local_path)
        print('successful firebase upload')

    @classmethod
    def get_url( self, child_path_to_file ):
        url = self.storage.child(child_path_to_file).get_url(None)
        return url

    @classmethod
    def update_last_stored_datetime( self, platform, datetime_string ):
        # Create a document within a collection
        result = self.firestore.child("last_posted_dates").set({
            platform.value: datetime_string
        })
        return result

    @classmethod
    def get_last_posted_datetime( self, platform ):
        # Retrieve the data from a collection
        # users = db.child("users").get().val()
        # print(users)

        # Retrieve the data from a document
        print(platform.value)
        document = self.firestore.child("last_posted_dates").child(platform.value)
        print(f'Document data: {document}')
        last_posted_datetime_str = document.get().val()
        print(f'Document data: {last_posted_datetime_str}')
        last_posted_datetime = datetime.datetime.fromisoformat(last_posted_datetime_str)
        return last_posted_datetime

    '''
        Get the actual post that we stored earlier in firebase document/JSON format

        Args:
            string platform: The value from our enum determing the platform we are working with
            string posting_time: Specific ISO formatted datetime used to fetch

        Returns:
            string. JSON string translated from the specific document fetched from firebase
    '''
    def get_specific_post( self, platform, posting_time ):
        specific_collection = f'{platform.value}_{self.POSTS_COLLECTION}'
        print(f'specific collection {specific_collection}')
        result = self.firestore.child(specific_collection).get()
        if result.each() is None:
            print("No document found with the specified property value.")
            return ''
        else:
            for document in result.each():
                if (document.key() == posting_time):
                    document_json = json.dumps(document.val())
                    return document_json

    def upload_scheduled_post( self, platform, payload ):
        last_posted_time = self.get_last_posted_datetime(platform)
        future_publish_date = scheduler.get_best_posting_time(platform, last_posted_time)
        update_success = self.update_last_stored_datetime( platform, future_publish_date )
        print(f'update_success {update_success}')

        specific_collection = platform.value + "_" + self.POSTS_COLLECTION
        result = self.firestore.child(specific_collection).set({
            future_publish_date: payload
        })
        print('firebase upload result')
        print(result)
        return result
