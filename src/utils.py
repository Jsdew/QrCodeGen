# src/utils.py
import logging
import os
from urllib.parse import urlparse
from typing import Any, Dict
import re

def validate_url(url: str) -> None:
    """
    Validate the given URL to ensure it starts with 'http://' or 'https://'.

    Parameters:
        url (str): The URL to validate.

    Raises:
        ValueError: If the URL is invalid.
    """
    parsed_url = urlparse(url)
    if parsed_url.scheme not in ('http', 'https'):
        logging.error(f"Invalid URL scheme: {url}")
        raise ValueError("Invalid URL. It must start with 'http://' or 'https://'.")

    if not parsed_url.netloc:
        logging.error(f"Invalid URL domain: {url}")
        raise ValueError("Invalid URL. It must contain a valid domain.")

    logging.info(f"URL validated: {url}")

def ensure_directory_exists(directory_path: str) -> None:
    """
    Ensure that the specified directory exists. Create it if it does not.

    Parameters:
        directory_path (str): The path to the directory to check or create.
    """
    if not os.path.exists(directory_path):
        logging.info(f"Creating directory: {directory_path}")
        os.makedirs(directory_path, exist_ok=True)

def sanitize_file_path(file_path: str) -> str:
    """
    Sanitize the file path to remove any invalid characters or sequences.

    Parameters:
        file_path (str): The file path to sanitize.

    Returns:
        str: A sanitized file path.
    """
    sanitized_path = os.path.normpath(file_path)
    logging.debug(f"Sanitized file path: {sanitized_path}")
    return sanitized_path

def validate_color(color: str) -> bool:
    """
    Validate if the provided string is a valid hex color code.

    Parameters:
        color (str): The color code to validate.

    Returns:
        bool: True if the color is a valid hex code, False otherwise.
    """
    pattern = re.compile(r'^#(?:[0-9a-fA-F]{3}){1,2}$')
    if pattern.match(color):
        logging.info(f"Valid color code: {color}")
        return True
    else:
        logging.error(f"Invalid color code: {color}")
        return False

def validate_configuration(config: Dict[str, Any]) -> None:
    """
    Validate the configuration dictionary.

    Parameters:
        config (Dict[str, Any]): Configuration data to validate.

    Raises:
        ValueError: If required configuration fields are missing or invalid.
    """
    logging.debug("Validating configuration.")
    required_sections = ['data', 'output', 'appearance', 'qr_code']
    for section in required_sections:
        if section not in config:
            logging.error(f"Missing required section: {section}")
            raise ValueError(f"Missing required section: {section}")

    if 'url' not in config['data']:
        logging.error("Missing 'url' in 'data' section.")
        raise ValueError("Missing 'url' in 'data' section.")

    if 'output_format' not in config['output']:
        logging.warning("'output_format' not specified. Defaulting to 'PNG'.")
        config['output']['output_format'] = 'PNG'

    if 'gradient' not in config['appearance']:
        logging.warning("'gradient' not specified. Defaulting to disabled.")
        config['appearance']['gradient'] = {'enabled': False, 'start_color': 'black', 'end_color': 'black'}

    logging.info("Configuration validated successfully.")
