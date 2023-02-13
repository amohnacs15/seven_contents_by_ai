# Instagram
import json
import requests
import appsecrets

def get_fb_credentials():
	""" Get creds required for use in the applications
	
	Returns:
		dictonary: credentials needed globally
	"""

	creds = dict() # dictionary to hold everything
	creds['access_token'] = appsecrets.META_SHORT_LIVED_USER_ID_TOKEN # access token for use with all api calls
	creds['graph_domain'] = 'https://graph.facebook.com/' # base domain for api calls
	creds['graph_version'] = 'v15.0' # version of the api we are hitting
	creds['endpoint_base'] = creds['graph_domain'] + creds['graph_version'] + '/' # base endpoint with domain and version
	creds['debug'] = 'no'

	return creds	

#Reuse this facebook and instagram
def make_api_call( url, endpointParams, type ) :
	""" Request data from endpoint with params
	
	Args:
		url: string of the url endpoint to make request from
		endpointParams: dictionary keyed by the names of the url parameters
	Returns:
		object: data from the endpoint
	"""

	if type == 'POST' : # post request
		data = requests.post( url, endpointParams )
	else : # get request
		data = requests.get( url, endpointParams )

	response = dict() # hold response info
	response['url'] = url # url we are hitting
	
	response['endpoint_params'] = endpointParams #parameters for the endpoint
	response['endpoint_params_pretty'] = json.dumps( endpointParams, indent = 4 ) # pretty print for cli

	response['json_data'] = json.loads( data.content ) # response data from the api
	response['json_data_pretty'] = json.dumps( response['json_data'], indent = 4 ) # pretty print for cli

	return response # get and return content

def display_api_call_data( response ) :
	""" Print out to cli response from api call """

	print ("\nURL: ") # title
	print (response['url']) # display url hit
	print ("\nEndpoint Params: ") # title
	print (response['endpoint_params_pretty']) # display params passed to the endpoint
	print ("\nResponse: ") # title
	print (response['json_data_pretty']) # make look pretty for cli	