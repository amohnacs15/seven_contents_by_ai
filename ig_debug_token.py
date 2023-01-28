from ig_definition import getCreds, makeApiCall
import datetime

def getIgDebugAccessToken() :
	
    params = getCreds()
    params['debug'] = 'yes' # set debug

    endpointParams = dict() # parameter to send to the endpoint
    endpointParams['input_token'] = params['access_token'] # input token is the access token
    endpointParams['access_token'] = params['access_token'] # access token to get debug info on

    url = params['graph_domain'] + '/debug_token' # endpoint url

    response = makeApiCall( url, endpointParams, params['debug'] ) # make the api call

    print("\nData Access Expires at: ") # label
    print(datetime.datetime.fromtimestamp( response['json_data']['data']['data_access_expires_at'] )) # display out when the token expires

    print("\nToken Expires at: ") # label
    print(datetime.datetime.fromtimestamp( response['json_data']['data']['expires_at'] )) # display out when the token expires

    return response

