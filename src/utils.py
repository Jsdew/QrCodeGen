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

    data_section = config['data']
    # Ensure at least one URL is provided
    if not any(data_section.get(key) for key in ['website', 'instagram', 'tiktok']):
        logging.error("At least one URL must be provided in 'data' section (website, instagram, or tiktok).")
        raise ValueError("At least one URL must be provided in 'data' section (website, instagram, or tiktok).")

    output_section = config['output']
    # Validate output paths
    for key in ['qr_code_path', 'logo_path', 'final_path']:
        if key not in output_section:
            logging.error(f"Missing '{key}' in 'output' section.")
            raise ValueError(f"Missing '{key}' in 'output' section.")

    if 'output_format' not in output_section:
        logging.warning("'output_format' not specified. Defaulting to 'PNG'.")
        output_section['output_format'] = 'PNG'

    appearance_section = config['appearance']
    # Validate appearance settings
    for key in ['fill_color', 'back_color', 'logo_size_ratio', 'padding']:
        if key not in appearance_section:
            logging.error(f"Missing '{key}' in 'appearance' section.")
            raise ValueError(f"Missing '{key}' in 'appearance' section.")

    if 'gradient' not in appearance_section:
        logging.warning("'gradient' not specified. Defaulting to disabled.")
        appearance_section['gradient'] = {'enabled': False, 'start_color': 'black', 'end_color': 'black'}

    qr_code_section = config['qr_code']
    # Validate QR code settings
    qr_code_keys = ['version', 'error_correction', 'box_size', 'border', 'width', 'height']
    for key in qr_code_keys:
        if key not in qr_code_section:
            logging.error(f"Missing '{key}' in 'qr_code' section.")
            raise ValueError(f"Missing '{key}' in 'qr_code' section.")

    logging.info("Configuration validated successfully.")
