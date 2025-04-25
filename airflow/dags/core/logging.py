# airflow/dags/core/logging.py
import logging
import sys

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = logging.INFO # Consider making this configurable (e.g., via Airflow Variable)

def get_task_logger(name: str) -> logging.Logger:
    """
    Creates and configures a logger instance for use within Airflow tasks or DAGs.

    Args:
        name (str): The name for the logger, typically __name__ of the calling module.

    Returns:
        logging.Logger: A configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # Avoid adding multiple handlers if logger already configured
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout) # Log to stdout, Airflow will capture it
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # Prevent logs from propagating to the root logger if Airflow handles it
    logger.propagate = False

    return logger

# Example usage within a task callable:
# from .logging import get_task_logger
# logger = get_task_logger(__name__)
# logger.info("Starting task...")
