# logging_setup.py
import logging
import os
import time


def initialize_logging(node_id: int, extra_dir: str = None):
    """
    Initializes both the default and per-node logging setup.

    Args:
        node_id (int): Unique identifier for the node.
        extra_dir (str): Optional additional directory for the logs.
    """
    # Get the base directory path for the logs
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Generate the timestamp
    timestamp = time.strftime("%Y%m%d%H%M%S")

    # Define log directory and create a subdirectory for the current timestamp
    log_dir = os.path.join(base_dir, "../../../../logs")
    if extra_dir:
        log_dir = os.path.join(log_dir, extra_dir, timestamp)
    else:
        log_dir = os.path.join(log_dir, f"log_{timestamp}")
    os.makedirs(log_dir, exist_ok=True)

    # Create a default log file within the timestamped directory
    default_log_file = os.path.join(log_dir, "log_default.log")

    # Set up the default logger
    logging.basicConfig(
        filename=default_log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    default_logger = logging.getLogger("default_logger")

    # Create a log file specific to this node within the timestamped directory
    node_log_file = os.path.join(log_dir, f"log_node{node_id}.log")

    # Set up the per-node logger
    node_logger = logging.getLogger(f"Node_{node_id}")
    node_logger.setLevel(logging.DEBUG)  # Set to the desired logging level

    # Create a file handler for the node-specific logger
    node_handler = logging.FileHandler(node_log_file)
    node_handler.setLevel(logging.DEBUG)  # Set to the desired logging level

    # Create a common formatter
    formatter = logging.Formatter(
        "%(asctime)s - Node %(node_id)d - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    node_handler.setFormatter(formatter)

    # Add the handler to the per-node logger
    node_logger.addHandler(node_handler)

    return default_logger, node_logger
