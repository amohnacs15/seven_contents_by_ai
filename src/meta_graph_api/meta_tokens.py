import sys
import os
sys.path.append("../src")

from meta_graph_api.meta_definition import make_api_call
import appsecrets
import json
from storage.firebase_storage import firebase_storage_instance, PostingPlatform

def create_ig_access_token_creds():
	""" Get creds required for use in the applications
	
	Returns:
		dictonary: credentials needed globally
	"""
	creds = dict() # dictionary to hold everything
	creds['access_token'] = appsecrets.IG_SHORT_LIVED_USER_ID_TOKEN # access token for use with all api calls
	creds['client_id'] = appsecrets.META_APP_ID
	creds['client_secret'] = appsecrets.META_APP_SECRET
	creds['graph_domain'] = 'https://graph.facebook.com/' # base domain for api calls
	creds['graph_version'] = 'v15.0' # version of the api we are hitting
	creds['endpoint_base'] = creds['graph_domain'] + creds['graph_version'] + '/' # base endpoint with domain and version
	creds['instagram_account_id'] = appsecrets.INSTAGRAM_GRAPH_API_PAGE_ID # users instagram account id
	creds['debug'] = 'no'

	return creds

""" Get long lived access token
	
	API Endpoint:
		https://graph.facebook.com/{graph-api-version}/oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={your-access-token}
	Returns:
		object: data from the endpoint
"""
def get_ig_access_creds() :

    params = create_ig_access_token_creds()
    cachedToken = firebase_storage_instance.get_token(PostingPlatform.INSTAGRAM)

    if (cachedToken != ''):
        params['access_token'] = cachedToken
        print(f"IG found cached token!")
        
        return params
    else:
        get_token_params = dict() # parameter to send to the endpoint
        get_token_params['grant_type'] = 'fb_exchange_token' # tell facebook we want to exchange token
        get_token_params['client_id'] = params['client_id'] # client id from facebook app
        get_token_params['client_secret'] = params['client_secret'] # client secret from facebook app
        get_token_params['fb_exchange_token'] = params['access_token'] # access token to get exchange for a long lived token

        token_url = params['endpoint_base'] + 'oauth/access_token' # endpoint url
        token_response = make_api_call( url=token_url, endpointParams=get_token_params, type=params['debug'] ) # make the api call
        
        print(token_response['json_data'])
        access_token = token_response['json_data']['access_token']
        firebase_storage_instance.store_token(PostingPlatform.INSTAGRAM, access_token)

        print("\n ---- ACCESS TOKEN INFO ----\n") # section header
        print("Access Token:")  # label
        print(access_token)
        pretty_dump = json.dumps( token_response['json_data'], indent = 4 ) 
        print(pretty_dump)

        params['access_token'] = access_token

    return params

def get_fb_page_access_token():
    cachedToken = firebase_storage_instance.get_token(PostingPlatform.FACEBOOK)

    if (cachedToken != ''):
        params = dict()
        params['graph_domain'] = 'https://graph.facebook.com/' # base domain for api calls
        params['graph_version'] = 'v15.0' # version of the api we are hitting
        params['endpoint_base'] = params['graph_domain'] + params['graph_version'] + '/'
        params['page_access_token'] = cachedToken

        print("found cached page access token!")
        print(params['page_access_token'])
        
        return params
    else:
        params = get_fb_credentials()
        post_url = params['endpoint_base'] + appsecrets.FACEBOOK_GRAPH_API_PAGE_ID
        
        params['fields'] = 'access_token'
        params['access_token'] = params['access_token']

        response = make_api_call( url=post_url, endpointParams=params, type='GET' )
        params['page_access_token'] = response['json_data']['access_token']
        firebase_storage_instance.store_token(PostingPlatform.FACEBOOK, params['page_access_token'])

    return params

def get_fb_credentials():
	""" Get creds required for use in the applications
	
	Returns:
		dictonary: credentials needed globally
	"""

	creds = dict() # dictionary to hold everything
	creds['access_token'] = appsecrets.FB_PAGE_SHORT_LIVED_USER_ID_TOKEN # access token for use with all api calls
	creds['graph_domain'] = 'https://graph.facebook.com/' # base domain for api calls
	creds['graph_version'] = 'v15.0' # version of the api we are hitting
	creds['endpoint_base'] = creds['graph_domain'] + creds['graph_version'] + '/' # base endpoint with domain and version
	creds['debug'] = 'no'

	return creds	