from typing import List

import pymongo

from .mongo import create_client
from .log import get_logger

logger = get_logger(__name__)


def store(
    statuses: List[dict],
    client: pymongo.MongoClient = None,
    database="test",
    collection="tweets",
) -> List[str]:
    if client is None:
        client = create_client()

    db = client[database]
    tweets = db[collection]

    logger.info({"op": "evaluate-statuses"})
    statuses = list(statuses)

    logger.info({"op": "insert-tweets", "amount": len(statuses)})
    result = tweets.insert_many(statuses)

    logger.info({"op": "insert-tweets-done"})

    return result.inserted_ids
