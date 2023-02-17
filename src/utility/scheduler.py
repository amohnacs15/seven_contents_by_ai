import sys
sys.path.append("../src")

import datetime
import storage.firebase_storage as firebase_storage

facebook_times_array = [
    '0001-01-01T08:00:00', #8am
    '0001-01-01T10:00:00', #10am
    '0001-01-01T12:00:00', #12pm
    '0001-01-01T14:00:00', #2pm
    '0001-01-01T16:00:00', #4pm
    '0001-01-01T18:00:00'  #6pm
]
instagram_times_array = [
    '0001-01-01T09:00:00', #9am
    '0001-01-01T11:00:00', #11am
    '0001-01-01T13:00:00', #1pm
    '0001-01-01T15:00:00', #3pm
    '0001-01-01T17:00:00', #5pm
    '0001-01-01T19:00:00' #7pm
]
youtube_times_array = [
    '0001-01-01T09:00:00', #9am
    '0001-01-01T16:00:00', #4pm
    '0001-01-01T19:00:00' #7pm
]

'''
    Reads the last posted time and gets the next one.  Then we write to file and return ISO value

    Params:
        platform: Enum that we use to determine which file to get

    Returns:
        string in the ISO 8601 format "%Y-%m-%dT%H:%M:%S+0000"
        example: "scheduled_publish_time": "2023-02-20T00:00:00+0000"
'''
def get_best_posting_time( 
    posting_platform,
    last_posted_time
):
    print('last_posting_time')
    print(last_posted_time)
    if (posting_platform == firebase_storage.PostingPlatform.FACEBOOK):
        times_array = facebook_times_array
    elif (posting_platform == firebase_storage.PostingPlatform.YOUTUBE):
        times_array = youtube_times_array
    else:
        #this will need to be updated
        times_array = instagram_times_array

    for str_posting_time in times_array:
        potential_posting_time = datetime.datetime.fromisoformat(str_posting_time)
        potential_posting_time = potential_posting_time.replace(
            year=last_posted_time.year, 
            month=last_posted_time.month, 
            day=last_posted_time.day
        )
        # we have found the time after what was last posted
        if (last_posted_time < potential_posting_time):
            str_posting_time = potential_posting_time.strftime("%Y-%m-%dT%H:%M:%S")
            return str_posting_time

    # This means we need to go to the next day. Get the first posting time tomorrow   
    potential_tomorrow_posting_time = last_posted_time + datetime.timedelta(days=1)    
    tomorrow_posting_time = datetime.datetime.fromisoformat(times_array[0])
    str_posting_time = tomorrow_posting_time.replace(
        year = potential_tomorrow_posting_time.year,
        month=potential_tomorrow_posting_time.month,
        day=potential_tomorrow_posting_time.day
    )
    print('tomorrow posting time: ' + str(str_posting_time))
    str_posting_time = str_posting_time.strftime("%Y-%m-%dT%H:%M:%S")
    return str_posting_time      


# def get_facebook_posting_datetime_in_epoch():
#     assert PlatformDateStore.FACEBOOK.value != ''

#     with open(PlatformDateStore.FACEBOOK.value, 'r') as file:
#         line = file.read()
#         last_posted_time = datetime.datetime.fromisoformat(line.strip())
#         print('last posted time: ' + str(last_posted_time))
#         posting_time = get_best_posting_time(
#             posting_platform = firebase_storage.PostingPlatform.FACEBOOK,
#             last_posted_time=last_posted_time, 
#             file_path= PlatformDateStore.FACEBOOK.value, 
#             times_array=facebook_times_array
#         )
#         epoch_posting_time = int(posting_time.timestamp())
#         return epoch_posting_time           

def datetime_to_epoch(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    epoch_int = int((dt - epoch).total_seconds() * 1000)
    return epoch_int

def get_youtube_posting_datetime():
    assert PostingPlatform.YOUTUBE.value != ''

    with open(PostingPlatform.YOUTUBE.value, 'r') as file:
        line = file.read()
        last_posted_time = datetime.datetime.fromisoformat(line.strip())
        print('last posted time: ' + str(last_posted_time))
        posting_time = get_best_posting_time(
            posting_platform=PostingPlatform.YOUTUBE,
            last_posted_time=last_posted_time, 
            file_path=PostingPlatform.YOUTUBE.value,
            times_array=youtube_times_array
        )
        return posting_time     