import pyrebase
import appsecrets
from enum import Enum
import json
from firebase_admin import firebase
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
    db = firebase.database()

    @classmethod
    def upload_mp3( remote_storage_path, local_path ):
        firebase.storage().child(remote_storage_path).put(local_path)
        print('successful firebase upload')

    @classmethod
    def get_url( child_path_to_file ):
        url = firebase.storage().child(child_path_to_file).get_url(None)
        return url

    @classmethod
    def update_last_stored_datetime( self, platform, datetime_string ):

        # Create a document within a collection
        self.db.child("last_posted_times").set({
            "platform": platform,
            "last_posted_datetime": datetime_string
        })

    @classmethod
    def get_last_posted_datetime( self, platform ):
        # Retrieve the data from a collection
        # users = db.child("users").get().val()
        # print(users)

        # Retrieve the data from a document
        last_posted_datetime = self.db.child("last_posted_times").child(platform).get().val()
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
        result = self.db.child(specific_collection).order_by_child("scheduled_post_datetime").equal_to(posting_time).get()

        if result.each() is None:
            print("No document found with the specified property value.")
            return ''
        else:
            for document in result.each():
                document_json = json.dumps(document)
                return document_json

    def upload_scheduled_post( self, platform, payload ):
        last_posted_time = self.get_last_posted_datetime(platform)
        future_publish_date = scheduler.get_best_posting_time(platform,last_posted_time)
        self.update_last_stored_datetime( platform, future_publish_date )

        specific_collection = platform + "_" + self.POSTS_COLLECTION
        result = self.db.child(specific_collection).set({
            "scheduled_datetime": future_publish_date,
            "body": payload
        })
        return result
