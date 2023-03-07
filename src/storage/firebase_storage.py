import sys
sys.path.append("../src")

import pyrebase
import appsecrets as appsecrets
from enum import Enum
import json
import utility.scheduler as scheduler
import utility.time_utils as time_utils
from datetime import datetime

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
    TOKEN_COLLECTION = "tokens"
    META_LF_TOKEN_COLLECTION = "meta_long_form_tokens" 
    META_SF_TOKEN_COLLECTION = "meta_short_form_one_hour_tokens" 

    # Initializations    
    firebase = pyrebase.initialize_app(appsecrets.firebase_config)
    firestore = firebase.database()
    storage = firebase.storage()

    @classmethod
    def get_meta_short_lived_token(self, platform):
        results = self.firestore.child(self.TOKEN_COLLECTION).child(self.META_SF_TOKEN_COLLECTION).get()
        if (results.each() is not None):
            for result in results.each():
                if (result.key() == platform.value): return result.val()
        return '' 

    @classmethod
    def store_meta_bearer_token(self, platform, token):
        result = self.firestore.child(self.TOKEN_COLLECTION).child(self.META_LF_TOKEN_COLLECTION).update({
            platform.value: token
        })
        return result

    @classmethod
    def get_meta_bearer_token(self, platform):
        results = self.firestore.child(self.TOKEN_COLLECTION).child(self.META_LF_TOKEN_COLLECTION).get()
        if (results.each() is not None):
            for result in results.each():
                if (result.key() == platform.value): return result.val()
        return ''    

    @classmethod
    def delete_storage_file(self, remote_storage_path):
        result = self.storage.child(remote_storage_path).delete()
        print(f'successful firebase storage delete {result}')

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
            print(f'{platform} earliest scheduled datetime not found')
            return ''
        if (len(collection) > 0):
            earliest_scheduled_datetime_str = collection[0].key()
            return earliest_scheduled_datetime_str

            # if (time_utils.is_expired(earliest_scheduled_datetime_str)):
            #     self.delete_post(platform, earliest_scheduled_datetime_str)
            #     self.get_earliest_scheduled_datetime(platform)
            # else:
            #     return earliest_scheduled_datetime_str
        else:
            print(f'{platform} something went wrong with get_earliest_scheduled_datetime( self, platform )')  
            return ''

    @classmethod
    def get_latest_scheduled_datetime( self, platform ):
        scheduled_posts_path = platform.value + self.POSTS_COLLECTION_APPEND_PATH

        collection = self.firestore.child(scheduled_posts_path).get().each()
        if (collection is None):
            return scheduler.get_best_posting_time(
                platform,
                time_utils.get_datetime_now()
            )
        if (len(collection) > 0):
            latest_scheduled_datetime_str = collection[len(collection) - 1].key().strip()
            print(f'{platform} latest_scheduled_datetime_str: {latest_scheduled_datetime_str}')

            formatted_iso = time_utils.convert_str_to_iso_format(latest_scheduled_datetime_str)
            latest_scheduled_datetime = datetime.fromisoformat(formatted_iso)
            return latest_scheduled_datetime
        else:
            print(f'{platform} something went wrong with get_latest_scheduled_datetime( self, platform )')  
            return ''  

    @classmethod
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

    @classmethod
    def upload_scheduled_post( self, platform, payload ):
        last_posted_time = self.get_latest_scheduled_datetime(platform)
        if (last_posted_time == '' or last_posted_time is None):
            last_posted_time = time_utils.get_datetime_now()
            print(f'{platform} last_posted_time was empty, setting to now: {type(last_posted_time)}')

        future_publish_date = scheduler.get_best_posting_time(platform, last_posted_time)

        specific_collection = platform.value + "_" + self.POSTS_COLLECTION
        result = self.firestore.child(specific_collection).update({
            future_publish_date: payload
        })
        print(f'{platform} firebase upload result\n{result}')
        return result

    @classmethod
    def delete_post( self, platform, datetime_key ):
        scheduled_posts_path = platform.value + self.POSTS_COLLECTION_APPEND_PATH
        result = self.firestore.child(scheduled_posts_path).child(datetime_key).remove()
        print(f'{platform} firebase delete result \n{result}')
        return result

#static instances
firebase_storage_instance = FirebaseStorage()