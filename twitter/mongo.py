"""MongoDB client.

See Also
--------
- PyMongo docs: https://api.mongodb.com/python/current/api/pymongo/index.html
"""
import os

import dotenv
import pymongo

dotenv.load_dotenv()


def create_client():
    """Build and return an instance of the MongoDB Atlas client.

    See Also
    --------
    https://docs.atlas.mongodb.com/driver-connection/#driver-examples
    """
    user = os.environ["MONGO_USER"]
    password = os.environ["MONGO_PASSWORD"]
    cluster = os.environ["MONGO_CLUSTER"]
    srv = (
        f"mongodb+srv://{user}:{password}@{cluster}.mongodb.net"
        "/test?retryWrites=true"
    )
    client = pymongo.MongoClient(srv)

    return client
