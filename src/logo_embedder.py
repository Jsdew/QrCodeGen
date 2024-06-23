from PIL import Image, ImageDraw
import logging
import os
from .file_utils import ensure_directory_exists, save_image

def add_logo_to_qr(qr_img: Image.Image, logo_path: str, output_path: str,
                   logo_size_ratio: int = 5, padding: int = 10, shape: str = 'square') -> None:
    """
    Add a logo to the center of the QR code.

    Parameters:
        qr_img (Image.Image): The QR code image.
        logo_path (str): Path to the logo image file.
        output_path (str): Path to save the QR code with the logo.
        logo_size_ratio (int): Ratio to determine the size of the logo.
        padding (int): Padding around the logo.
        shape (str): Shape of the logo area ('circle', 'square').

    Raises:
        FileNotFoundError: If the logo file does not exist.
        ValueError: If an unsupported shape is provided.
    """
    logging.info(f"Adding logo from {logo_path} to QR code with shape {shape}")
    if not os.path.exists(logo_path):
        logging.error(f"Logo file not found: {logo_path}")
        raise FileNotFoundError(f"Logo file not found: {logo_path}")

    logo = Image.open(logo_path).convert("RGBA")
    qr_width, qr_height = qr_img.size
    logo_size = (qr_width // logo_size_ratio, qr_height // logo_size_ratio)
    logo = logo.resize(logo_size, Image.LANCZOS)

    # Calculate the position to paste the logo
    pos = ((qr_width - logo.size[0]) // 2, (qr_height - logo.size[1]) // 2)

    # Create a mask for the logo based on the shape
    mask = Image.new('L', logo.size, 0)
    draw = ImageDraw.Draw(mask)
    if shape == 'circle':
        draw.ellipse((0, 0, logo.size[0], logo.size[1]), fill=255)
    elif shape == 'square':
        draw.rectangle((0, 0, logo.size[0], logo.size[1]), fill=255)
    else:
        raise ValueError("Unsupported shape. Supported shapes are 'circle' and 'square'.")

    # Create a central area in the QR code based on the shape and padding
    area_mask = Image.new('L', qr_img.size, 0)
    draw = ImageDraw.Draw(area_mask)
    if shape == 'circle':
        circle_diameter = logo.size[0] + padding
        draw.ellipse(
            ((qr_width - circle_diameter) // 2, (qr_height - circle_diameter) // 2,
             (qr_width + circle_diameter) // 2, (qr_height + circle_diameter) // 2),
            fill=255
        )
    elif shape == 'square':
        square_size = logo.size[0] + padding
        draw.rectangle(
            ((qr_width - square_size) // 2, (qr_height - square_size) // 2,
             (qr_width + square_size) // 2, (qr_height + square_size) // 2),
            fill=255
        )

    # Apply the area mask to create a clean center
    qr_img_with_area = qr_img.copy()
    qr_img_with_area.paste((255, 255, 255), (0, 0), area_mask)

    # Paste the logo using the mask
    qr_img_with_area.paste(logo, pos, mask)

    # Ensure directory exists before saving
    ensure_directory_exists(os.path.dirname(output_path))
    save_image(qr_img_with_area, output_path)
    logging.info(f"QR code with logo saved to: {output_path}")
