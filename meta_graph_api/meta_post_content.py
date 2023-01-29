import time
from meta_graph_api.meta_definition import makeApiCall
import appsecrets
import meta_tokens as meta_tokens
import requests


def createIgMediaObject( params ) :
	""" Create media object

	Args:
		params: dictionary of params
	
	API Endpoint:
		https://graph.facebook.com/v5.0/{ig-user-id}/media?image_url={image-url}&caption={caption}&access_token={access-token}
		https://graph.facebook.com/v5.0/{ig-user-id}/media?video_url={video-url}&caption={caption}&access_token={access-token}

	Returns:
		object: data from the endpoint

	"""

	url = params['endpoint_base'] + params['instagram_account_id'] + '/media' # endpoint url

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['caption'] = params['caption']  # caption for the post
	endpointParams['access_token'] = params['access_token'] # access token

	if 'IMAGE' == params['media_type'] : # posting image
		endpointParams['image_url'] = params['media_url']  # url to the asset
	else : # posting video
		endpointParams['media_type'] = params['media_type']  # specify media type
		endpointParams['video_url'] = params['media_url']  # url to the asset
	
	return makeApiCall( url, endpointParams, 'POST' ) # make the api call

def getIgMediaObjectStatus( mediaObjectId, params ) :
	""" Check the status of a media object

	Args:
		mediaObjectId: id of the media object
		params: dictionary of params
	
	API Endpoint:
		https://graph.facebook.com/v5.0/{ig-container-id}?fields=status_code

	Returns:
		object: data from the endpoint

	"""

	url = params['endpoint_base'] + '/' + mediaObjectId # endpoint url

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['fields'] = 'status_code' # fields to get back
	endpointParams['access_token'] = params['access_token'] # access token

	return makeApiCall( url, endpointParams, 'GET' ) # make the api call

def publishIgMedia( mediaObjectId, params ) :
	""" Publish content

	Args:
		mediaObjectId: id of the media object
		params: dictionary of params
	
	API Endpoint:
		https://graph.facebook.com/v5.0/{ig-user-id}/media_publish?creation_id={creation-id}&access_token={access-token}

	Returns:
		object: data from the endpoint

	"""

	url = params['endpoint_base'] + params['instagram_account_id'] + '/media_publish' # endpoint url

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['creation_id'] = mediaObjectId # fields to get back
	endpointParams['access_token'] = params['access_token'] # access token

	return makeApiCall( url, endpointParams, 'POST' ) # make the api call

def getContentPublishingLimit( params ) :
	""" Get the api limit for the user

	Args:
		params: dictionary of params
	
	API Endpoint:
		https://graph.facebook.com/v5.0/{ig-user-id}/content_publishing_limit?fields=config,quota_usage

	Returns:
		object: data from the endpoint

	"""

	url = params['endpoint_base'] + params['instagram_account_id'] + '/content_publishing_limit' # endpoint url

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['fields'] = 'config,quota_usage' # fields to get back
	endpointParams['access_token'] = params['access_token'] # access token

	return makeApiCall( url, endpointParams, 'GET' ) # make the api call

def sendIgImagePost( media_url, caption ):
    params = meta_tokens.getIgLongLivedAccessCreds() # get creds from defines
    
    params['media_type'] = 'IMAGE' # type of asset
    params['media_url'] = 'https://justinstolpe.com/sandbox/ig_publish_content_img.png' # url on public server for the post
    params['caption'] = caption

    imageMediaObjectResponse = createIgMediaObject( params ) # create a media object through the api
    print(imageMediaObjectResponse)
    imageMediaObjectId = imageMediaObjectResponse['json_data']['id'] # id of the media object that was created
    imageMediaStatusCode = 'IN_PROGRESS';

    print( "\n---- IMAGE MEDIA OBJECT -----\n" ) # title
    print( "\tID:" ) # label
    print( "\t" + imageMediaObjectId ) # id of the object

    while imageMediaStatusCode != 'FINISHED' : # keep checking until the object status is finished
        imageMediaObjectStatusResponse = getIgMediaObjectStatus( imageMediaObjectId, params ) # check the status on the object
        imageMediaStatusCode = imageMediaObjectStatusResponse['json_data']['status_code'] # update status code

        print( "\n---- IMAGE MEDIA OBJECT STATUS -----\n" ) # display status response
        print( "\tStatus Code:" ) # label
        print( "\t" + imageMediaStatusCode ) # status code of the object

        time.sleep( 5 ) # wait 5 seconds if the media object is still being processed

    publishImageResponse = publishIgMedia( imageMediaObjectId, params ) # publish the post to instagram

    print( "\n---- PUBLISHED IMAGE RESPONSE -----\n" ) # title
    print( "\tResponse:" ) # label
    print( publishImageResponse['json_data_pretty'] ) # json response from ig api

def sendIgVideoPost( media_url, caption ):

    params = meta_tokens.getIgLongLivedAccessCreds() # get creds from defines

    params['media_type'] = 'VIDEO' # type of asset
    params['media_url'] = media_url # url on public server for the post
    params['caption'] = caption

    videoMediaObjectResponse = createIgMediaObject( params ) # create a media object through the api
    videoMediaObjectId = videoMediaObjectResponse['json_data']['id'] # id of the media object that was created
    videoMediaStatusCode = 'IN_PROGRESS';

    print( "\n---- VIDEO MEDIA OBJECT -----\n" ) # title
    print( "\tID:" ) # label
    print( "\t" + videoMediaObjectId ) # id of the object

    while videoMediaStatusCode != 'FINISHED' : # keep checking until the object status is finished
        videoMediaObjectStatusResponse = getIgMediaObjectStatus( videoMediaObjectId, params ) # check the status on the object
        videoMediaStatusCode = videoMediaObjectStatusResponse['json_data']['status_code'] # update status code

        print( "\n---- VIDEO MEDIA OBJECT STATUS -----\n" ) # display status response
        print( "\tStatus Code:" ) # label
        print( "\t" + videoMediaStatusCode ) # status code of the object

        time.sleep( 5 ) # wait 5 seconds if the media object is still being processed

    publishVideoResponse = publishIgMedia( videoMediaObjectId, params ) # publish the post to instagram

    print( "\n---- PUBLISHED IMAGE RESPONSE -----\n" ) # title
    print( "\tResponse:" ) # label
    print( publishVideoResponse['json_data_pretty'] ) # json response from ig api

    contentPublishingApiLimit = getContentPublishingLimit( params ) # get the users api limit

    print( "\n---- CONTENT PUBLISHING USER API LIMIT -----\n" ) # title
    print( "\tResponse:" ) # label
    print( contentPublishingApiLimit['json_data_pretty'] ) # json response from ig api

def sendFbImagePost( filename, post ):
	# token = meta_tokens.getIgAccessToken('facebook')

	post_url = 'https://graph.facebook.com/{}/feed'.format(appsecrets.FACEBOOK_GRAPH_API_PAGE_ID)
	image_location = 'http://image.careers-portal.co.za/f_output.jpg'
	payload = {
		'message': post,
		'access_token': "token"
	}
	#Send the POST request
	r = requests.post(post_url, data=payload)
	print(r.text)	