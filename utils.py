import logging
import os

path = os.getcwd()
if not os.path.isdir("logs"):
    os.mkdir("logs")


def setup_logging(log_level, test_name):
    logger = logging.getLogger(__name__)
    logger_handler = logging.FileHandler(f"logs/{test_name}.log", mode="a")
    logger.setLevel(level=log_level)
    logger_formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y/%m/%d %H:%M:%S")
    logger_handler.setFormatter(logger_formatter)
    logger.addHandler(logger_handler)
    return logger
