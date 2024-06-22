from src.qr_generator import generate_qr_code
from src.image_utils import apply_gradient, apply_background_image
from src.logo_embedder import add_logo_to_qr
from src.utils import validate_url, validate_configuration
from src.config import load_config, get_config_path
from src.logger import configure_logging, log_execution_time
from src.file_utils import ensure_directory_exists  
import logging
import os

# Initialize logging
configure_logging()

@log_execution_time
def main() -> None:
    """
    Main function to load configuration and generate QR codes for each URL.
    """
    try:
        config_path = get_config_path()
        config = load_config(config_path)
        validate_configuration(config)

        data_section = config['data']
        website = data_section.get('website')
        instagram = data_section.get('instagram')
        tiktok = data_section.get('tiktok')

        # Ensure at least one URL is provided
        if not any([website, instagram, tiktok]):
            raise ValueError("At least one URL must be provided in 'data' section (website, instagram, or tiktok).")

        # Validate URLs
        if website:
            validate_url(website)
        if instagram:
            validate_url(instagram)
        if tiktok:
            validate_url(tiktok)

        # Base file name
        base_name = os.path.basename(website or instagram or tiktok).replace('https://', '').replace('http://', '').replace('/', '')

        logging.info("Starting QR code generation...")

        def generate_and_save_qr(data: str, service_name: str):
            file_path = f"./files/output/{service_name}@{base_name}_QR.png"
            output_path = f"./files/output_logo/{service_name}@{base_name}_QR_with_logo.png"

            # Ensure directories exist
            ensure_directory_exists(os.path.dirname(file_path))
            ensure_directory_exists(os.path.dirname(output_path))

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

            logging.info(f"Adding logo to the {service_name} QR code...")
            add_logo_to_qr(qr_img, config['output']['logo_path'], output_path, logo_size_ratio=logo_size_ratio, padding=padding)

            logging.info(f"{service_name} QR code saved as {output_path}")

        # Generate QR codes for each URL
        if website:
            generate_and_save_qr(website, 'Website')
        if instagram:
            generate_and_save_qr(instagram, 'Instagram')
        if tiktok:
            generate_and_save_qr(tiktok, 'TikTok')

    except ValueError as ve:
        logging.error(f"Configuration error: {ve}")
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")

if __name__ == '__main__':
    main()
