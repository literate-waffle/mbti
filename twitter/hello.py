"""Hello Tweepy!

From:
https://tweepy.readthedocs.io/en/3.7.0/getting_started.html
"""

import os
import tweepy
import dotenv

dotenv.load_dotenv()


def create_api():
    auth = tweepy.OAuthHandler(
        os.getenv("TWITTER_CONSUMER_KEY"), os.getenv("TWITTER_CONSUMER_SECRET")
    )
    auth.set_access_token(
        os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_TOKEN_SECRET")
    )
    return tweepy.API(auth)


def main():
    api = create_api()
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)


if __name__ == "__main__":
    main()
