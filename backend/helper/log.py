import logging


def setup_logging():
    # Check if the logger has already been set up
    logger = logging.getLogger(__name__)
    if logger.hasHandlers():
        # Logger has already been set up, return the existing instance
        return logger

    # Create a logger instance
    logger.setLevel(logging.INFO)

    # Create a file handler to write log messages to a file
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.INFO)

    # Create a stream handler to output log messages to the terminal
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    # Create a log formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',  datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # Add the file handler and stream handler to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
