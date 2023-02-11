import datetime
from enum import Enum
import utility.utils as utils

# _underscore means private
_facebook_store_path = 'storage_files/facebook_scheduler_store.txt'
_instagram_store_path = 'storage_files/facebook_scheduler_store.txt'
_youtube_store_path = 'storage_files/facebook_scheduler_store.txt'

class PlatformDateStore(Enum):
    FACEBOOK = _facebook_store_path
    INSTAGRAM = _instagram_store_path
    YOUTUBE = _youtube_store_path


facebook_times_array = [
    '0001-01-01T08:00:00', #8am
    '0001-01-01T10:00:00', #10am
    '0001-01-01T12:00:00', #12pm
    '0001-01-01T14:00:00', #2pm
    '0001-01-01T16:00:00', #4pm
    '0001-01-01T18:00:00'  #6pm
]
instagram_times_array = [
    '09:00:00', #9am
    '11:00:00', #11am
    '13:00:00', #1pm
    '15:00:00', #3pm
    '17:00:00', #5pm
    '19:00:00' #7pm
]
youtube_times_array = [
    '09:00:00', #9am
    '16:00:00', #4pm
    '19:00:00' #7pm
]

@classmethod
def compare_times(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        time1 = datetime.datetime.fromisoformat(lines[0].strip())
        time2 = datetime.datetime.strptime(lines[1].strip(), '%H:%M')
        time2 = time2.replace(year=time1.year, month=time1.month, day=time1.day)

    if time1 < time2:
        return "Time 1 is earlier"
    elif time1 > time2:
        return "Time 2 is earlier"
    else:
        return "Both times are equal"        

'''
    Reads the last posted time from a file and gets the next one.  Then we write to file and return ISO value

    Params:
        platform: Enum that we use to determine which file to get

    Returns:
        string in the ISO 8601 format "%Y-%m-%dT%H:%M:%S+0000"
        example: "scheduled_publish_time": "2023-02-20T00:00:00+0000"
'''
def get_next_posting_date_in_iso_format(platform):
    if (platform == PlatformDateStore.FACEBOOK):
        assert PlatformDateStore.FACEBOOK.value != ''

        with open(PlatformDateStore.FACEBOOK.value, 'r') as file:
            line = file.read()
            last_posted_time = datetime.datetime.fromisoformat(line.strip())
            print('last posted time: ' + str(last_posted_time))

            for posting_time in facebook_times_array:
                print('read from array: ' + posting_time)
                potential_posting_time = datetime.datetime.fromisoformat(posting_time)
                potential_posting_time = potential_posting_time.replace(
                    year=last_posted_time.year, 
                    month=last_posted_time.month, 
                    day=last_posted_time.day
                )
                # we have found the time after what was last posted
                print("comparing last_posted_time ")
                print(last_posted_time)
                print(" to potential time ")
                print(potential_posting_time)

                if (last_posted_time < potential_posting_time):
                    posting_time = potential_posting_time.strftime("%Y-%m-%dT%H:%M:%S")
                    utils.save_file(PlatformDateStore.FACEBOOK.value, posting_time)
                    return posting_time

            # This means we need to go to the next day. Get the first posting time tomorrow   
            potential_tomorrow_posting_time = last_posted_time + datetime.timedelta(days=1)    
            tomorrow_posting_time = datetime.datetime.fromisoformat(facebook_times_array[0])
            posting_time = tomorrow_posting_time.replace(
                year = potential_tomorrow_posting_time.year,
                month=potential_tomorrow_posting_time.month,
                day=potential_tomorrow_posting_time.day
            )
            print('tomorrow postint time: ' + str(posting_time))
            str_posting_time = posting_time.strftime("%Y-%m-%dT%H:%M:%S")
            utils.save_file(PlatformDateStore.FACEBOOK.value, str_posting_time)
            return posting_time
                    
    elif (platform == PlatformDateStore.INSTAGRAM):
        assert PlatformDateStore.INSTAGRAM.value != ''

        # the above code needs to be put into a method and ported here
    elif (platform == PlatformDateStore.YOUTUBE):
        assert PlatformDateStore.YOUTUBE.value != ''

        # the above code needs to be put into a method and ported here
    else:
        print('Something went wrong.  Platform not considered.')            