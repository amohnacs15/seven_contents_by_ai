import sys
sys.path.append("../src")

import pyrebase
import appsecrets as appsecrets
from enum import Enum
import json
import utility.scheduler as scheduler
import datetime
import utility.time_utils as time_utils

class PostingPlatform(Enum):
        FACEBOOK = 'facebook'
        INSTAGRAM = 'instagram'
        TWITTER = 'twitter'
        YOUTUBE = 'youtube'
        SHOPIFY = 'shopify'

class FirebaseStorage():
    # Constants
    POSTS_COLLECTION = "posts"
    POSTS_COLLECTION_APPEND_PATH = "_posts"

    # Initializations    
    firebase = pyrebase.initialize_app(appsecrets.firebase_config)
    firestore = firebase.database()
    storage = firebase.storage()

    @classmethod
    def upload_mp3( self, remote_storage_path, local_path ):
        result = self.storage.child(remote_storage_path).put(local_path)
        print(f'successful firebase storage upload {result}')

    @classmethod
    def get_url( self, child_path_to_file ):
        url = self.storage.child(child_path_to_file).get_url(None)
        return url

    @classmethod
    def get_earliest_scheduled_datetime( self, platform ):
        scheduled_posts_path = platform.value + self.POSTS_COLLECTION_APPEND_PATH

        collection = self.firestore.child(scheduled_posts_path).get().each()
        if (collection is None):
            return ''
        if (len(collection) > 0):
            earliest_scheduled_datetime_str = collection[0].key()
            return earliest_scheduled_datetime_str
        else:
            print('something went wrong with get_earliest_scheduled_datetime( self, platform )')  
            return ''

    @classmethod
    def get_latest_scheduled_datetime( self, platform ):
        scheduled_posts_path = platform.value + self.POSTS_COLLECTION_APPEND_PATH

        collection = self.firestore.child(scheduled_posts_path).get().each()
        if (collection is None):
            return scheduler.get_best_posting_time(
                platform,
                datetime.datetime.now()
            )
        if (len(collection) > 0):
            latest_scheduled_datetime_str = collection[len(collection) - 1].key().strip()
            print(f'latest_scheduled_datetime_str: {latest_scheduled_datetime_str}')

            formatted_iso = time_utils.convert_str_to_iso_format(latest_scheduled_datetime_str)
            latest_scheduled_datetime = datetime.datetime.fromisoformat(formatted_iso)
            return latest_scheduled_datetime
        else:
            print('something went wrong with get_latest_scheduled_datetime( self, platform )')  
            return ''  

    
    def get_specific_post( self, platform, posting_time ):
        '''
            Get the actual post that we stored earlier in firebase document/JSON format

            Args:
                string platform: The value from our enum determing the platform we are working with
                string posting_time: Specific ISO formatted datetime used to fetch

            Returns:
                string. JSON string translated from the specific document fetched from firebase
        '''
        specific_collection = f'{platform.value}_{self.POSTS_COLLECTION}'
        result = self.firestore.child(specific_collection).get()
        if result.each() is None:
            return "No document found with the specified property value."
        else:
            for document in result.each():
                print(f'{specific_collection} result: {result.key()} -> {result.val()}')
                if (document.key() == posting_time):
                    document_json = json.dumps(document.val())
                    return document_json

    def upload_scheduled_post( self, platform, payload ):
        last_posted_time = self.get_latest_scheduled_datetime(platform)
        print(f'last_posted_time: {last_posted_time}')
        if (last_posted_time == ''):
            last_posted_time = datetime.datetime.now()
            print(f'last_posted_time was empty, setting to now: {type(last_posted_time)}')

        future_publish_date = scheduler.get_best_posting_time(platform, last_posted_time)

        specific_collection = platform.value + "_" + self.POSTS_COLLECTION
        result = self.firestore.child(specific_collection).update({
            future_publish_date: payload
        })
        print(f'firebase upload result\n{result}')
        return result

    def delete_post( self, platform, datetime_key ):
        scheduled_posts_path = platform.value + self.POSTS_COLLECTION_APPEND_PATH
        result = self.firestore.child(scheduled_posts_path).child(datetime_key).remove()
        print(f'firebase delete result \n{result}')
        return result

#static instances
firebase_storage_instance = FirebaseStorage()