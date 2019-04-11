import json
from typing import List

from .log import get_logger

logger = get_logger(__name__)


def store(statuses: List[dict], dest: str) -> List[str]:
    logger.info({"op": "evaluate-statuses"})
    statuses = list(statuses)

    logger.info({"op": "write-tweets", "amount": len(statuses)})
    with open(dest, "w") as dest_file:
        dest_file.write(json.dumps(statuses))

    logger.info({"op": "write-tweets-done"})
