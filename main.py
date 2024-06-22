# main.py
from src.qr_generator import generate_qr_code
from src.image_utils import apply_gradient, apply_background_image
from src.logo_embedder import add_logo_to_qr
from src.utils import validate_url, validate_configuration
from src.config import load_config, get_config_path
from src.logger import configure_logging, log_execution_time
import logging
from typing import Any, Dict
import os

# Initialize logging
configure_logging()

@log_execution_time
def main() -> None:
    """
    Main function to load configuration and generate a single QR code.
    """
    try:
        config_path = get_config_path()
        config = load_config(config_path)
        validate_configuration(config)

        data = config['data']['url']
        validate_url(data)

        logging.info("Starting QR code generation...")

        file_path = config['output']['qr_code_path']
        logo_path = config['output']['logo_path']
        output_path = config['output']['final_path']
        output_format = config['output']['output_format']

        fill_color = config['appearance']['fill_color']
        back_color = config['appearance']['back_color']
        logo_size_ratio = config['appearance']['logo_size_ratio']
        padding = config['appearance']['padding']
        foreground_pattern = config['appearance'].get('foreground_pattern', 'squares')
        gradient = config['appearance'].get('gradient')

        qr_code_config = config['qr_code']
        version = qr_code_config['version']
        error_correction = qr_code_config['error_correction']
        box_size = qr_code_config['box_size']
        border = qr_code_config['border']
        width = qr_code_config['width']
        height = qr_code_config['height']
        quiet_zone = qr_code_config['quiet_zone']
        background_image = qr_code_config.get('background_image')
        scale = qr_code_config['scale']

        qr_img = generate_qr_code(
            data,
            fill_color=fill_color,
            back_color=back_color,
            version=version,
            box_size=box_size,
            border=border,
            width=width,
            height=height,
            error_correction=error_correction,
            quiet_zone=quiet_zone,
            scale=scale
        )

        # Apply gradient if enabled
        if gradient and gradient.get('enabled'):
            qr_img = apply_gradient(qr_img, gradient['start_color'], gradient['end_color'])

        # Apply background image if provided
        if background_image and os.path.exists(background_image):
            qr_img = apply_background_image(qr_img, background_image)

        logging.info("Adding logo to the QR code...")
        add_logo_to_qr(qr_img, logo_path, output_path, logo_size_ratio=logo_size_ratio, padding=padding)

    except ValueError as ve:
        logging.error(f"Configuration error: {ve}")
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")

if __name__ == '__main__':
    main()
