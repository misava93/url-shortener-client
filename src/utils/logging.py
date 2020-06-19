import logging
from datetime import datetime

FORMATTER_DEFAULT = logging.Formatter("%(asctime)s [%(levelname)s] %(module)s - %(funcName)s: %(message)s")
LOG_FILEPATH_DEFAULT = "/tmp/{}_skillshare_url_shortener_client.log"
LOG_LEVEL_DEFAULT = logging.INFO


def get_filepath():
    return LOG_FILEPATH_DEFAULT.format(datetime.now().strftime("%d-%m-%YT%H"))


def get_logger(name: str, filepath: str = get_filepath(), formatter: logging.Formatter = FORMATTER_DEFAULT,
               level: int = LOG_LEVEL_DEFAULT) -> logging.Logger:
    # setup a file handler
    file_handler = logging.FileHandler(filepath)
    file_handler.setFormatter(formatter)

    # setup a console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # get logger, set level and attach handlers
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
