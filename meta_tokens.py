from meta_graph_api.meta_definition import makeApiCall
import appsecrets
import utility.utils as utils
import json
import requests

def getIgTempCredentials() :
	""" Get creds required for use in the applications
	
	Returns:
		dictonary: credentials needed globally
	"""
	creds = dict() # dictionary to hold everything
	creds['access_token'] = appsecrets.META_SHORT_LIVED_USER_ID_TOKEN # access token for use with all api calls
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
def getLongLivedAccessCreds() :

    params = getIgTempCredentials()
    cachedToken = utils.open_file("ig_access_token.txt")

    if (cachedToken != ''):
        print("found cached token!")
        params['access_token'] = cachedToken
        return params
    else:
        endpointParams = dict() # parameter to send to the endpoint
        endpointParams['grant_type'] = 'fb_exchange_token' # tell facebook we want to exchange token
        endpointParams['client_id'] = params['client_id'] # client id from facebook app
        endpointParams['client_secret'] = params['client_secret'] # client secret from facebook app
        endpointParams['fb_exchange_token'] = params['access_token'] # access token to get exchange for a long lived token

        url = params['endpoint_base'] + 'oauth/access_token' # endpoint url

        response = makeApiCall( url, endpointParams, params['debug'] ) # make the api call
        access_token = response['json_data']['access_token']

        print("\n ---- ACCESS TOKEN INFO ----\n") # section header
        print("Access Token:")  # label
        utils.save_file("ig_access_token.txt", access_token) 

        params['access_token'] = access_token

        return params

def getFbPageAccessToken ( ):
    params = getLongLivedAccessCreds()
    post_url = params['endpoint_base'] + appsecrets.FACEBOOK_GRAPH_API_PAGE_ID
    
    params['fields'] = 'access_token'
    params['access_token'] = params['access_token']

    response = makeApiCall( post_url, params, 'GET' )
    params['page_access_token'] = response['json_data']['access_token']

    return params
