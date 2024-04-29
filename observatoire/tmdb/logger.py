import logging


def setup_logger() -> logging:
    # Create a logger for the current module
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Define the log format
    log_formatter = logging.Formatter(
        "%(asctime)s    | %(name)s  | %(levelname)s | %(message)s",
    )

    # Create a stream handler to output log messages to the console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)
    logger.addHandler(stream_handler)

    return logger
