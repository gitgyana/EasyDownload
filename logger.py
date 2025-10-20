import os
import logging
from datetime import datetime

log_dir = os.path.join('logs', datetime.now().strftime("%Y.%m"))
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y.%m.%d_%H.%M.%S')}.log")

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ],
)

def log(level: str, message: str) -> None:
    """
    Log a message with the given level.

    Parameters:
        level (str): Logging level as a string. 
                     Examples: 'debug', 'info', 'warning', 'error', 'critical'.
                     Case-insensitive.
        message (str): The message to log.

    Returns:
        None
    """
    level = level.upper()
    numeric_level = getattr(logging, level, logging.INFO)
    logging.log(numeric_level, message)
