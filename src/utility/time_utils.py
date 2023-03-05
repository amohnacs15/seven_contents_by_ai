from datetime import datetime, timedelta
import utility.time_utils as time_utils
import pytz

_est_timezone=pytz.timezone('America/New_York')

def get_datetime_now():
    return datetime.now(_est_timezone)

def is_current_posting_time_within_window( earliest_scheduled_datetime_str ):
    '''
        Allow for a threshold of a minute in each direction of the scheduled time to allow and honest
        check of whether or not we are running this at the time of a scheduled post.

        Params:
            datetime scheduled_time:  the remotely stored value of when we have calculated our next posting should be
            datetime current_time: the time we have started the run of this app

        Returns:
            boolean: are we running this close enough to the scheduled date
    '''
    formatted_iso=time_utils.convert_str_to_iso_format(earliest_scheduled_datetime_str.strip())
    scheduled_time=datetime.fromisoformat(formatted_iso)
    current_time=get_datetime_now()
    print(current_time)
    
    lower_bound=scheduled_time - timedelta(minutes=5)
    upper_bound=scheduled_time + timedelta(minutes=5)

    print(f'Checking if {current_time} is between {lower_bound} and {upper_bound}')
    if lower_bound.timestamp() < current_time.timestamp() < upper_bound.timestamp():
        print('Yes, it is. Posting now.')
        return True
    else:
        print('No, it is not. Not posting now.')
        return False

def convert_str_to_iso_format(date_str):
    """
    Converts a date string in the format '%Y-%m-%d %H:%M:%S' to the ISO format '%Y-%m-%dT%H:%M:%S'.

    Args:
        date_str (str): The input date string to be converted.

    Returns:
        str: The converted date string in ISO format, or None if an error occurs.
    """
    try:
        # First, parse the input string to create a datetime object
        date_obj=datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        # Then, format the datetime object to the desired ISO format
        iso_format_str=date_obj.strftime("%Y-%m-%dT%H:%M:%S")
        return iso_format_str

    except ValueError as e:
        # If the input string is not in the expected format, catch the ValueError exception
        # and return None
        return date_str
