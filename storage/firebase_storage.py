import pyrebase
import appsecrets
from enum import Enum
import json
import firebase_admin
import utility.scheduler as scheduler

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
            "platform": platform.value,
            "last_posted_datetime": datetime_string
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
        last_posted_datetime = document.get().val()
        print(f'Document data: {last_posted_datetime}')
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
        specific_collection = platform + "_" + self.POSTS_COLLECTION
        result = self.firestore.child(specific_collection).order_by_child("scheduled_post_datetime").equal_to(posting_time).get()

        if result.each() is None:
            print("No document found with the specified property value.")
            return ''
        else:
            for document in result.each():
                document_json = json.dumps(document)
                return document_json

    def upload_scheduled_post( self, platform, payload ):
        last_posted_time = self.get_last_posted_datetime(platform)
        print('last posted time')
        print(last_posted_time)
        future_publish_date = scheduler.get_best_posting_time(platform,last_posted_time)
        ('future publishing time')
        (future_publish_date)
        success = self.update_last_stored_datetime( platform, future_publish_date )
        print(success)

        specific_collection = platform.value + "_" + self.POSTS_COLLECTION
        print('specific collection')
        print(specific_collection)
        result = self.firestore.child(specific_collection).set({
            "scheduled_datetime": future_publish_date,
            "body": payload
        })
        print('firebase upload result')
        print(result)
        return result
