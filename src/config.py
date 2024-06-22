# src/config.py
from pathlib import Path
import yaml
import os
import logging
from typing import Any, Dict, Union
from yaml.parser import ParserError
from yaml.scanner import ScannerError

def load_config(file_path: str = 'config/settings.yaml') -> Dict[str, Any]:
    """
    Loads the configuration from a YAML file.

    Parameters:
        file_path (str): Path to the configuration file.

    Returns:
        dict: Parsed configuration data.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        ValueError: If there is an error parsing the YAML file.
    """
    config_path = Path(file_path)
    
    if not config_path.exists():
        logging.error(f"Configuration file not found: {file_path}")
        raise FileNotFoundError(f"Configuration file not found: {file_path}")

    try:
        with config_path.open('r') as file:
            config = yaml.safe_load(file)
            validate_config(config)  # Validate config structure
            return config
    except (ParserError, ScannerError) as e:
        logging.error(f"Error parsing the YAML configuration file: {file_path}")
        logging.exception(e)
        raise ValueError(f"Error parsing the YAML configuration file: {file_path}") from e
    except Exception as e:
        logging.error(f"Unexpected error loading configuration: {file_path}")
        logging.exception(e)
        raise

def validate_config(config: Dict[str, Any]) -> None:
    """
    Validates the configuration dictionary structure.

    Parameters:
        config (dict): Configuration data to validate.

    Raises:
        ValueError: If the configuration structure is invalid.
    """
    required_keys = ['data', 'output', 'appearance', 'qr_code']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required configuration section: {key}")

    # Validate 'data' section
    if 'url' not in config['data']:
        raise ValueError("Missing 'url' in 'data' section.")

    # Validate 'output' section
    for key in ['qr_code_path', 'logo_path', 'final_path']:
        if key not in config['output']:
            raise ValueError(f"Missing '{key}' in 'output' section.")

    # Validate 'appearance' section
    for key in ['fill_color', 'back_color', 'logo_size_ratio', 'padding']:
        if key not in config['appearance']:
            raise ValueError(f"Missing '{key}' in 'appearance' section.")

    # Validate 'qr_code' section
    qr_code_keys = ['version', 'error_correction', 'box_size', 'border', 'width', 'height']
    for key in qr_code_keys:
        if key not in config['qr_code']:
            raise ValueError(f"Missing '{key}' in 'qr_code' section.")

    # Additional specific checks can be added here, e.g., checking value ranges

def get_config_path() -> str:
    """
    Retrieves the configuration file path, allowing for an environment variable override.

    Returns:
        str: Path to the configuration file.
    """
    return os.getenv('CONFIG_PATH', 'config/settings.yaml')
