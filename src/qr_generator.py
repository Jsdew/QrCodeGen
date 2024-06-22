# src/qr_generator.py
import qrcode
from PIL import Image
import logging
from typing import Optional, Dict, Any

def generate_qr_code(data: str, fill_color: str = 'black', back_color: str = 'white',
                     version: int = 1, box_size: int = 10, border: int = 4,
                     width: int = 300, height: int = 300, error_correction: str = 'H',
                     quiet_zone: int = 4, scale: float = 1.0) -> Image.Image:
    """
    Generate a QR code image.

    Parameters:
        data (str): The data to encode in the QR code.
        fill_color (str): Foreground color of the QR code.
        back_color (str): Background color of the QR code.
        version (int): QR code version (1 to 40).
        box_size (int): Size of each QR box (pixels).
        border (int): Size of QR code border (in boxes).
        width (int): Width of the QR code image (pixels).
        height (int): Height of the QR code image (pixels).
        error_correction (str): Error correction level ('L', 'M', 'Q', 'H').
        quiet_zone (int): Minimum quiet zone width (modules).
        scale (float): Scaling factor for the entire QR code.

    Returns:
        Image.Image: The generated QR code image.
    """
    logging.info(f"Generating QR code for data: {data}")
    qr = qrcode.QRCode(
        version=version,
        error_correction=getattr(qrcode.constants, f'ERROR_CORRECT_{error_correction}'),  # Convert 'H' to qrcode.constants.ERROR_CORRECT_H
        box_size=box_size,
        border=max(border, quiet_zone),  # Ensure the border is at least as large as the quiet zone
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGBA')
    img = img.resize((int(width * scale), int(height * scale)), Image.LANCZOS)
    return img
