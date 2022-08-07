import tweepy
import logging
import requests


class TwitterOperations:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, bearerToken):
        self.logger = logging.getLogger("tweepy")
        self.logger.setLevel(logging.DEBUG)
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        handler = logging.FileHandler(filename="tweepy.log")
        self.logger.addHandler(handler)

        auth = tweepy.OAuth1UserHandler(
            self.consumer_key, self.consumer_secret, self.access_token, self.access_token_secret)
        self.api = tweepy.API(auth)

        self.bearer_header = {
            'Accept-Encoding': 'gzip',
            'Authorization': 'Bearer {}'.format(bearerToken)
        }

    def postTweet(self, tweet):
        post_result = self.api.update_status(status=tweet)
        self.logger.info(post_result)

    def postTweetWithMedia(self, tweet, mediaFilePath):
        media = self.api.media_upload(mediaFilePath)
        post_result = self.api.update_status(
            status=tweet, media_ids=[media.media_id])
        self.logger.info(post_result)

    def replyStatusWithImage(self, text, id, mediaFilePath):
        media = self.api.media_upload(mediaFilePath)
        post_result = self.api.update_status(text,
                                             in_reply_to_status_id=id, media_ids=[media.media_id])
        self.logger.info(post_result)

    def getUserTweets(self, user_id):

        uri = f'https://api.twitter.com/2/users/{user_id}/tweets?tweet.fields=conversation_id,in_reply_to_user_id&user.fields=username,name'
        print(f"uri::{uri}")
        resp = requests.get(uri, headers=self.bearer_header)
        print(f'{"getUserTweets::"}{resp.json()}')

        return resp.json()

    def getTweet(self, id):
        uri = f'https://api.twitter.com/2/tweets/{id}?tweet.fields=conversation_id,in_reply_to_user_id'
        print(f"uri::{uri}")
        bearer_header = self.bearer_header
        resp = requests.get(uri, headers=bearer_header)
        print(f'{"resp:::"}{resp.json()}')
        return resp.json()

    def getConversation(self, conversation_id):
        uri = f'https://api.twitter.com/2/tweets/search/recent?query=conversation_id:{conversation_id}&tweet.fields=in_reply_to_user_id,conversation_id,author_id'

        print(f'conversations_uri::{uri}')
        bearer_header = self.bearer_header
        resp = requests.get(uri, headers=bearer_header)
        return resp.json()

    def getUser(self, user_id):
        uri = f'https://api.twitter.com/2/users/{user_id}'
        bearer_header = self.bearer_header
        resp = requests.get(uri, headers=bearer_header)
        return resp.json()
