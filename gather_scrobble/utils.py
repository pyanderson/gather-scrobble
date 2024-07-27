import logging


def get_logger(name: str, level: int = logging.INFO):
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter("[%(asctime)s][%(levelname)s] %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
