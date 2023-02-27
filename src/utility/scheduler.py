import sys
sys.path.append("../src")

import datetime
import storage.firebase_storage as firebase_storage
import utility.time_utils as time_utils

# 6 posts daily
# 2 posts per video
facebook_times_array = [
    '0001-01-01T08:00:00', #8am
    '0001-01-01T10:00:00', #10am
    '0001-01-01T12:00:00', #12pm
    '0001-01-01T14:00:00', #2pm
    '0001-01-01T16:00:00', #4pm
    '0001-01-01T18:00:00'  #6pm
]
# 6 posts daily
# 2 posts per video
instagram_times_array = [
    '0001-01-01T09:00:00', #9am
    '0001-01-01T11:00:00', #11am
    '0001-01-01T13:00:00', #1pm
    '0001-01-01T15:00:00', #3pm
    '0001-01-01T17:00:00', #5pm
    '0001-01-01T19:00:00' #7pm
]
# 3 videos per day
# 1 video per video
youtube_times_array = [
    '0001-01-01T09:00:00', #9am
    '0001-01-01T16:00:00', #4pm
    '0001-01-01T19:00:00' #7pm
]
# 48 tweets daily
# 16 tweets from 1 video
twitter_times_array = [
    '0001-01-01T00:00:00',
    '0001-01-01T00:30:00',
    '0001-01-01T01:00:00', 
    '0001-01-01T01:30:00', 
    '0001-01-01T02:00:00', 
    '0001-01-01T02:30:00', 
    '0001-01-01T03:00:00', 
    '0001-01-01T03:30:00', 
    '0001-01-01T04:00:00', 
    '0001-01-01T04:30:00', 
    '0001-01-01T05:00:00', 
    '0001-01-01T05:30:00', 
    '0001-01-01T06:00:00', 
    '0001-01-01T06:30:00', 
    '0001-01-01T07:00:00', 
    '0001-01-01T07:30:00', 
    '0001-01-01T08:00:00', 
    '0001-01-01T08:30:00', 
    '0001-01-01T09:00:00', 
    '0001-01-01T09:30:00', 
    '0001-01-01T10:00:00', 
    '0001-01-01T10:30:00', 
    '0001-01-01T11:00:00', 
    '0001-01-01T11:30:00', 
    '0001-01-01T12:00:00', 
    '0001-01-01T12:30:00', 
    '0001-01-01T13:00:00', 
    '0001-01-01T13:30:00', 
    '0001-01-01T14:00:00', 
    '0001-01-01T14:30:00', 
    '0001-01-01T15:00:00', 
    '0001-01-01T15:30:00', 
    '0001-01-01T16:00:00',
    '0001-01-01T16:30:00', 
    '0001-01-01T17:00:00', 
    '0001-01-01T17:30:00', 
    '0001-01-01T18:00:00', 
    '0001-01-01T18:30:00', 
    '0001-01-01T19:00:00', 
    '0001-01-01T19:30:00', 
    '0001-01-01T20:00:00', 
    '0001-01-01T20:30:00', 
    '0001-01-01T21:00:00', 
    '0001-01-01T21:30:00', 
    '0001-01-01T22:00:00', 
    '0001-01-01T22:30:00', 
    '0001-01-01T23:00:00', 
    '0001-01-01T23:30:00'
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
    if type(last_posted_time) == str:
        formatted_iso = time_utils.convert_str_to_iso_format(last_posted_time)
        last_posted_time = datetime.datetime.fromisoformat(formatted_iso)

    if (posting_platform == firebase_storage.PostingPlatform.FACEBOOK):
        times_array = facebook_times_array
    elif (posting_platform == firebase_storage.PostingPlatform.YOUTUBE):
        times_array = youtube_times_array
    elif (posting_platform == firebase_storage.PostingPlatform.TWITTER):
        times_array = twitter_times_array    
    else:
        #this will need to be updated for an error handling system
        times_array = instagram_times_array

    for str_posting_time in times_array:
        formatted_iso = time_utils.convert_str_to_iso_format(str_posting_time)
        potential_posting_time = datetime.datetime.fromisoformat(formatted_iso)
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
    formatted_iso = time_utils.convert_str_to_iso_format(times_array[0])
    tomorrow_posting_time = datetime.datetime.fromisoformat(formatted_iso)
    str_posting_time = tomorrow_posting_time.replace(
        year = potential_tomorrow_posting_time.year,
        month=potential_tomorrow_posting_time.month,
        day=potential_tomorrow_posting_time.day
    )
    print('tomorrow posting time: ' + str(str_posting_time))
    str_posting_time = str_posting_time.strftime("%Y-%m-%dT%H:%M:%S")
    return str_posting_time      
