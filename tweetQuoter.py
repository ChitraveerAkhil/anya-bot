
from tweepy import StreamingClient, StreamRule
from fileOperations import FileOperations
from twitterOperations import TwitterOperations
from quoteMaker import QuoteMaker

import sys


def initConfigFile():
    global configData
    configFilePath = FileOperations.parseFileName('configs', 'config.json')
    args = sys.argv
    if len(args) > 1:
        configFilePath = FileOperations.parseFileName(args[1], args[2])
    configData = FileOperations.initJsonFile(configFilePath)


def streamTweets():
    streamKey = 'Quote it @AnyaBot007'
    #streamKey = '#ManUtd'
    bearerToken = configData["bearerToken"]
    rule = StreamRule(streamKey)
    streaming_client = StreamListener(
        bearer_token=bearerToken, wait_on_rate_limit=True)

    streaming_client.add_rules(rule)
    streaming_client.delete_rules('1563248300052348930')
    print(streaming_client.get_rules())
    streaming_client.filter()


def main():
    initConfigFile()
    streamTweets()


class StreamListener(StreamingClient):

    def on_error(self, status_code):
        if status_code == 420:  # end of monthly limit rate (500k)
            return False

    def on_tweet(self, tweet):
        consumer_key = configData["consumerKey"]
        consumer_secret = configData["consumerSecretKey"]
        access_token = configData["accessToken"]
        access_token_secret = configData["accessSecretToken"]
        bearerToken = configData["bearerToken"]

        tweet_id = tweet.id
        #get replied userName
        tweetStr = tweet.text
        splits = tweetStr.split()
        client = TwitterOperations(
            consumer_key, consumer_secret, access_token, access_token_secret, bearerToken)
        #tweetById = client.getConverstionId(tweet.id,tweet_fields=['id', 'text', 'author_id', 'conversation_id', 'in_reply_to_user_id'])
        tweetResp = client.getTweet(tweet_id)
        data = tweetResp['data']

        conversationId = data['conversation_id']
        in_reply_to_user_id = data['in_reply_to_user_id']

        userTweets = client.getUserTweets(in_reply_to_user_id)
        user_tweet_conv_id = ''
        to_quote_tweet_txt = ''
        to_quote_tweet_id = ''
        count = 0
        for userTweet in userTweets['data']:
            user_tweet_conv_id = userTweet['conversation_id']
            if conversationId == user_tweet_conv_id:
                count += 1
                to_quote_tweet_txt = userTweet['text']
                to_quote_tweet_id = userTweet['id']

            if count > 1:
                break

        if count == 1:
            userDetails = client.getUser(in_reply_to_user_id)
            quoteMaker = QuoteMaker()
            mediaFilePath = FileOperations.parseFileName(
                'quoted_images', to_quote_tweet_id+'.png')
            quoteMaker.generate_image_with_quote(
                to_quote_tweet_txt, userDetails['data']['name'], mediaFilePath)

            client.replyStatusWithImage("Here's your Quote!",
                                        tweet_id, mediaFilePath)


if __name__ == "__main__":
    main()
