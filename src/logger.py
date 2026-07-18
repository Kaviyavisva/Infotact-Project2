"""
logger.py

Central logging configuration for the project.
"""

import logging


def get_logger(name: str):
    """
    Returns a configured logger instance.
    """

    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        handler.setFormatter(formatter)

        logger.addHandler(handler)

        logger.propagate = False

    return logger


def setup_logger():
    """
    Backward compatibility for older modules.
    """

    return get_logger("SupplyChainMonitor")