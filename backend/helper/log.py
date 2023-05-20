import logging


def setup_logging():
    # Check if the logger has already been set up
    logger = logging.getLogger(__name__)
    if logger.hasHandlers():
        # Logger has already been set up, return the existing instance
        return logger

    # Create a logger instance
    logger.setLevel(logging.INFO)

    # Create a stream handler to output log messages to the terminal
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    # Create a log formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',  datefmt='%Y-%m-%d %H:%M:%S')
    stream_handler.setFormatter(formatter)

    # Add the stream handler to the logger
    logger.addHandler(stream_handler)

    return logger
