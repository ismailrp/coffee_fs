import logging

from logging.handlers import RotatingFileHandler


def setup_logger(name, log_file, level=logging.INFO):

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    handler = RotatingFileHandler(
        log_file,
        maxBytes=5_000_000,
        backupCount=3
    )

    handler.setFormatter(formatter)

    logger = logging.getLogger(name)

    logger.setLevel(level)

    logger.addHandler(handler)

    return logger


app_logger = setup_logger(
    "app_logger",
    "logs/app.log"
)

error_logger = setup_logger(
    "error_logger",
    "logs/error.log",
    level=logging.ERROR
)

transaction_logger = setup_logger(
    "transaction_logger",
    "logs/transaction.log"
)