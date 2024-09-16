import logging
import os
import time


def initialize_logging(node_id: int, extra_dir: str = None):
    """
    Initializes the default, per-node, and key-specific logging setup.

    Args:
        node_id (int): Unique identifier for the node.
        extra_dir (str): Optional additional directory for the logs.
    """
    # Get the base directory path for the logs
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Generate the timestamp
    timestamp = time.strftime("%Y%m%d%H%M%S")

    # Define log directory and create a subdirectory for the current timestamp
    log_dir = os.path.join(base_dir, "../../logs")
    if extra_dir:
        log_dir = os.path.join(log_dir, extra_dir, f"log_{timestamp}")
    else:
        log_dir = os.path.join(log_dir, f"log_{timestamp}")
    os.makedirs(log_dir, exist_ok=True)

    # Set up the default logger
    default_logger = _setup_logger(
        "default_logger", os.path.join(log_dir, "log_default.log"), logging.INFO
    )

    node_logger = None
    if node_id >= 0:
        # Set up the node-specific logger
        node_logger = _setup_logger(
            f"Node_{node_id}",
            os.path.join(log_dir, f"log_node{node_id}.log"),
            logging.DEBUG,
        )

    # Set up the key-specific logger
    key_logger = _setup_logger(
        f"Key_{node_id}", os.path.join(log_dir, "log_key_stats.log"), logging.DEBUG
    )

    return default_logger, node_logger, key_logger


def _setup_logger(logger_name, log_file, level):
    """Helper function to set up individual loggers."""
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # Check if the logger already has handlers, and if so, avoid adding new ones
    if not logger.hasHandlers():
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger


def log_default_info(default_logger, message):
    """
    Logs an info message to the default logger.

    Args:
        message (str): The message to log.
    """
    default_logger.info(message)


def log_node_info(node_logger, message, node_id):
    """
    Logs an info message with the node_id included to the per-node logger.

    Args:
        message (str): The message to log.
        node_id (int): The node identifier for logging.
    """
    node_logger.info(message, extra={"node_id": node_id})


def log_key_statistics(key_logger, key_stats, step):
    """
    Logs key statistics with the node_id included to the key-specific logger.

    Args:
        key_logger (Logger): The key-specific logger.
        key_stats (dict): A dictionary with key statistics (key occurrence counts).
        node_id (int): The node identifier for logging.
    """
    key_logger.info(f"Key statistics for step {step}: {key_stats}")
