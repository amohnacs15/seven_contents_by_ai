# TWITTER
import tweepy
import src.appsecrets as appsecrets

def initialize_tweepy():
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(appsecrets.TWITTER_API_KEY, appsecrets.TWITTER_API_SECRET)
    auth.set_access_token(appsecrets.TWITTER_API_AUTH_TOKEN, appsecrets.TWITTER_API_AUTH_SECRET)

    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        print("Twitter Authentication OK")
    except:
        print("Error during Tweepy authentication") 
    return api    

def send_tweet( filePath, tweet ):
    tweepy_api = initialize_tweepy()
    
    # Using readlines()
    tweetFile = open(filePath, 'r', encoding="utf8")
    tweets = tweetFile.readlines()

    # Strips the newline character
    for tweet in tweets:
        if (tweet.strip()):
            try:
                tweepy_api.update_status(status = tweet)  
                print("Tweet sent:" + tweet)
            except:
                print('Tweet too long or error. Skipping')     