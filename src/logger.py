"""
logger.py

Central logging configuration for the project.
"""

import logging


def setup_logger():
    """
    Configure and return the project logger.
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

    return logging.getLogger("SupplyChainMonitor")