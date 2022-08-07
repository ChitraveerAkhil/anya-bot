import tweepy
import logging

class TwitterOperations:
    def __init__(self,consumer_key, consumer_secret, access_token, access_token_secret):
        self.logger = logging.getLogger("tweepy")
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(filename="tweepy.log")
        self.logger.addHandler(handler)

        auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret, access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def postTweet(self,tweet):
        post_result = self.api.update_status(status=tweet)
        self.logger.info(post_result)

    def postTweetWithMedia(self,tweet, mediaFilePath):
        media = self.api.media_upload(mediaFilePath)
        post_result = self.api.update_status(status=tweet, media_ids=[media.media_id])
        self.logger.info(post_result)
        