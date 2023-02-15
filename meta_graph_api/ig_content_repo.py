import time
import meta_graph_api.meta_tokens as meta_tokens
from meta_graph_api.meta_definition import make_api_call
import utility.utils as utils
import media.image_creator as image_creator
import utility.scheduler as scheduler
import storage.firebase_storage as local_storage


'''
Method called from main class that creates our endpoint request and makes the API call.
Also, prints status of uploading the payload.

@returns: nothing
'''
def send_ig_video_post( filename, caption ):
    params = meta_tokens.get_long_lived_access_creds() 

	# this needs to be fixed...obviously
    media_url = 'clever way to get our video'

    params['media_type'] = 'VIDEO' # type of asset
    params['media_url'] = media_url # url on public server for the post
    params['caption'] = caption

    videoMediaObjectResponse = create_ig_media_object( params ) # create a media object through the api
    videoMediaObjectId = videoMediaObjectResponse['json_data']['id'] # id of the media object that was created
    videoMediaStatusCode = 'IN_PROGRESS';

    print( "\n---- VIDEO MEDIA OBJECT -----\n" ) # title
    print( "\tID:" ) # label
    print( "\t" + videoMediaObjectId ) # id of the object

    while videoMediaStatusCode != 'FINISHED' : # keep checking until the object status is finished
        videoMediaObjectStatusResponse = get_ig_media_object_status( videoMediaObjectId, params ) # check the status on the object
        videoMediaStatusCode = videoMediaObjectStatusResponse['json_data']['status_code'] # update status code

        print( "\n---- VIDEO MEDIA OBJECT STATUS -----\n" ) # display status response
        print( "\tStatus Code:" ) # label
        print( "\t" + videoMediaStatusCode ) # status code of the object

        time.sleep( 5 ) # wait 5 seconds if the media object is still being processed

    publishVideoResponse = publish_ig_media( videoMediaObjectId, params ) # publish the post to instagram

    print( "\n---- PUBLISHED IMAGE RESPONSE -----\n" ) # title
    print( "\tResponse:" ) # label
    print( publishVideoResponse['json_data_pretty'] ) # json response from ig api

    contentPublishingApiLimit = get_content_publishing_limit( params ) # get the users api limit

    print( "\n---- CONTENT PUBLISHING USER API LIMIT -----\n" ) # title
    print( "\tResponse:" ) # label
    print( contentPublishingApiLimit['json_data_pretty'] ) # json response from ig api



""" Create media object

	Args:
		params: dictionary of params
	
	API Endpoint:
		https://graph.facebook.com/v5.0/{ig-user-id}/media?image_url={image-url}&caption={caption}&access_token={access-token}
		https://graph.facebook.com/v5.0/{ig-user-id}/media?video_url={video-url}&caption={caption}&access_token={access-token}

	Returns:
		object: data from the endpoint

"""
def create_ig_media_object( params ) :
	url = params['endpoint_base'] + params['instagram_account_id'] + '/media' # endpoint url

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['caption'] = params['caption']  # caption for the post
	endpointParams['access_token'] = params['access_token'] # access token
	endpointParams['published'] = False

	if 'IMAGE' == params['media_type'] : # posting image
		endpointParams['image_url'] = params['media_url']  # url to the asset
	else : # posting video
		endpointParams['media_type'] = params['media_type']  # specify media type
		endpointParams['video_url'] = params['media_url']  # url to the asset
	
	return make_api_call( url=url, endpointParams=endpointParams, type='POST' ) # make the api call

""" Check the status of a media object

	Args:
		mediaObjectId: id of the media object
		params: dictionary of params
	
	API Endpoint:
		https://graph.facebook.com/v5.0/{ig-container-id}?fields=status_code

	Returns:
		object: data from the endpoint

"""
def get_ig_media_object_status( mediaObjectId, params ) :
	url = params['endpoint_base'] + '/' + mediaObjectId # endpoint url

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['fields'] = 'status_code' # fields to get back
	endpointParams['access_token'] = params['access_token'] # access token

	return make_api_call( url=url, endpointParams=endpointParams, type='GET' ) # make the api call

""" Publish content

	Args:
		mediaObjectId: id of the media object
		params: dictionary of params
	
	API Endpoint:
		https://graph.facebook.com/v5.0/{ig-user-id}/media_publish?creation_id={creation-id}&access_token={access-token}

	Returns:
		object: data from the endpoint

"""
def publish_ig_media( mediaObjectId, params ) :
	url = params['endpoint_base'] + params['instagram_account_id'] + '/media_publish' # endpoint url

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['creation_id'] = mediaObjectId # fields to get back
	endpointParams['access_token'] = params['access_token'] # access token

	return make_api_call( url=url, endpointParams=endpointParams, type='POST' ) # make the api call

'''
Method called from main class that creates our endpoint request and makes the API call.
Also, prints status of uploading the payload.

@returns: nothing
'''
def send_ig_image_post( filename, caption ):
    params = meta_tokens.get_long_lived_access_creds() 
    
    params['media_type'] = 'IMAGE' 
	
    search_query = utils.get_title_subquery(caption)
    params['media_url'] = image_creator.get_unsplash_image_url(search_query) 
    params['caption'] = caption

    imageMediaObjectResponse = create_ig_media_object( params ) # create a media object through the api
    print(imageMediaObjectResponse)
    imageMediaObjectId = imageMediaObjectResponse['json_data']['id'] # id of the media object that was created
    imageMediaStatusCode = 'IN_PROGRESS'

    print( "\n---- IMAGE MEDIA OBJECT -----\n" ) # title
    print( "\tID:" ) # label
    print( "\t" + imageMediaObjectId ) # id of the object

    while imageMediaStatusCode != 'FINISHED' : # keep checking until the object status is finished
        imageMediaObjectStatusResponse = get_ig_media_object_status( imageMediaObjectId, params ) # check the status on the object
        imageMediaStatusCode = imageMediaObjectStatusResponse['json_data']['status_code'] # update status code

        print( "\n---- IMAGE MEDIA OBJECT STATUS -----\n" ) # display status response
        print( "\tStatus Code:" ) # label
        print( "\t" + imageMediaStatusCode ) # status code of the object

        time.sleep( 5 ) # wait 5 seconds if the media object is still being processed

    publishImageResponse = publish_ig_media( imageMediaObjectId, params ) # publish the post to instagram

    print( "\n---- PUBLISHED IMAGE RESPONSE -----\n" ) # title
    print( "\tResponse:" ) # label
    print( publishImageResponse['json_data_pretty'] ) # json response from ig api

""" Get the api limit for the user

	Args:
		params: dictionary of params
	
	API Endpoint:
		https://graph.facebook.com/v5.0/{ig-user-id}/content_publishing_limit?fields=config,quota_usage

	Returns:
		object: data from the endpoint

"""
def get_content_publishing_limit( params ) :
	url = params['endpoint_base'] + params['instagram_account_id'] + '/content_publishing_limit' # endpoint url

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['fields'] = 'config,quota_usage' # fields to get back
	endpointParams['access_token'] = params['access_token'] # access token

	return make_api_call( url=url, endpointParams=endpointParams, type='GET' ) # make the api call
