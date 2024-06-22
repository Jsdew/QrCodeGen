# src/logger.py
import os
import logging
import colorlog
from pathlib import Path
from time import time, strftime, gmtime
from typing import Optional

class SimpleFormatter(logging.Formatter):
    """Custom logging formatter without milliseconds."""
    
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        return strftime(datefmt or "%Y-%m-%d %H:%M:%S", ct)

def configure_logging(log_dir: str = 'logs', level: int = logging.DEBUG) -> None:
    """
    Set up logging configuration with colored console output and file logging.

    Parameters:
        log_dir (str): Directory to save log files.
        level (int): Logging level.

    Raises:
        OSError: If the log directory cannot be created.
    """
    try:
        Path(log_dir).mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise OSError(f"Unable to create log directory: {log_dir}") from e

    # Custom formatter without milliseconds
    log_formatter = SimpleFormatter(
        '%(asctime)s - %(module)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    color_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(module)s - %(levelname)s - %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'blue',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )

    # File handler for logging to file
    file_handler = logging.FileHandler(os.path.join(log_dir, 'qr_generator.log'))
    file_handler.setFormatter(log_formatter)

    # Console handler for logging to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(color_formatter)

    # Get the root logger and ensure only one instance of handlers
    logger = logging.getLogger()
    if not logger.hasHandlers():
        logger.setLevel(level)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    # Set the logging level for the PIL library
    pil_logger = logging.getLogger('PIL.Image')
    pil_logger.setLevel(logging.WARNING)  # Suppress debug logs for PIL

def log_execution_time(func):
    """Decorator to log the duration of a function."""
    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        duration = end_time - start_time
        logging.info(f"Execution time of {func.__name__}: {int(duration // 3600):02}:{int(duration % 3600 // 60):02}:{int(duration % 60):02}")
        return result
    return wrapper
