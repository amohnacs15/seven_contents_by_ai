from datetime import datetime, timedelta

'''
    Allow for a threshold of a minute in each direction of the scheduled time to allow and honest
    check of whether or not we are running this at the time of a scheduled post.

    Params:
        datetime scheduled_time:  the remotely stored value of when we have calculated our next posting should be
        datetime current_time: the time we have started the run of this app

    Returns:
        boolean: are we running this close enough to the scheduled date
'''
def is_current_posting_time_within_window( scheduled_time ):
    current_time = datetime.now()
    print(f'current time :{current_time}')
    
    lower_bound = scheduled_time - timedelta(minutes=5)
    upper_bound = scheduled_time + timedelta(minutes=5)

    if lower_bound < current_time < upper_bound:
        return True
    else:
        return False

