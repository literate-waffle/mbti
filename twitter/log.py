import logging


def get_logger(name: str, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    return logger
