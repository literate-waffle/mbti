# MBTI

MBTI prediction on Twitter.

## Install

You need Python 3.6+ installed.

- Install Python dependencies:

```bash
pip install -r requirements.txt
```

- Create a `.env` file in the project root directory. We use it to store private environment variables:

```bash
touch .env
```

### Connecting to Mongo Atlas

Tweets are stored in a MongoDB database via [Mongo Atlas](https://www.mongodb.com/cloud/atlas). To access the database, you'll need to have add the following environment variables:

```dotenv
MONGO_USER="..."
MONGO_PASSWORD="..."
MONGO_CLUSTER="..."
```

### Building the tweets database

This section only applies if you plan to rebuild the tweets database (MongoDB).

First, you'll need to get a [Twitter Developer account](https://developer.twitter.com) in order to get a consumer key and an access token.

Then, add the following environment variables:

```dotenv
TWITTER_CONSUMER_KEY="..."
TWITTER_CONSUMER_SECRET="..."
TWITTER_ACCESS_TOKEN="..."
TWITTER_TOKEN_SECRET="..."
```

Place the tweets CSV (e.g. `tweets.csv`) under the `data/` directory. **Make sure to remove the CSV header if there is one.**

Then run the following command:

```bash
python -m twitter data/tweets.csv
```
