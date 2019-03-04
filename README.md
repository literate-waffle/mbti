# Maple

MBTI prediction on Twitter.

## Install

```bash
pip install -r requirements.txt
```

### Retrieving tweets

This section only applies if you plan to rebuild the tweet database.

First, you'll need to get a [Twitter Developer account] in order to get a consumer key and an access token.

Then, create a `.env` file in the project root with the following variables:

```dotenv
TWITTER_CONSUMER_KEY="..."
TWITTER_CONSUMER_SECRET="..."
TWITTER_ACCESS_TOKEN="..."
TWITTER_TOKEN_SECRET="..."
```
