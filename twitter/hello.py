"""Hello Tweepy!

From:
https://tweepy.readthedocs.io/en/3.7.0/getting_started.html
"""

from .api import create_api


def main():
    api = create_api()
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)


if __name__ == "__main__":
    main()
