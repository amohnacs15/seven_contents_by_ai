import sys
sys.path.append("../src")

import pyrebase
import appsecrets as appsecrets
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
        result = self.firestore.child("last_posted_dates").update({
            platform.value: datetime_string
        })
        return result

    @classmethod
    def get_last_posted_datetime( self, platform ):

        # Retrieve the data from a document
        document = self.firestore.child("last_posted_dates").child(platform.value)
        last_posted_datetime_str = document.get().val()
        print(f'Document data: {platform} : {last_posted_datetime_str}')
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
                print(f'current doc: {document.key()} == {posting_time}')
                if (document.key() == posting_time):
                    document_json = json.dumps(document.val())
                    return document_json

    def upload_scheduled_post( self, platform, payload ):
        last_posted_time = self.get_last_posted_datetime(platform)
        assert last_posted_time != ''

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

firebase_storage_instance = FirebaseStorage()