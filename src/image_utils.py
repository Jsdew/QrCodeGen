from PIL import Image, ImageDraw
import logging

def hex_to_rgb(hex_color: str) -> tuple:
    """
    Convert a hex color code to an RGB tuple.

    Parameters:
        hex_color (str): The hex color code.

    Returns:
        tuple: The RGB color tuple.
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def apply_gradient(img: Image.Image, start_color: str, end_color: str) -> Image.Image:
    """
    Apply a gradient to the QR code image.

    Parameters:
        img (Image.Image): The QR code image.
        start_color (str): The starting color of the gradient.
        end_color (str): The ending color of the gradient.

    Returns:
        Image.Image: The QR code image with the gradient applied.
    """
    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)
    logging.info(f"Applying gradient from {start_rgb} to {end_rgb}")

    gradient = Image.new('RGBA', img.size, color=0)
    draw = ImageDraw.Draw(gradient)

    for y in range(img.height):
        r = int(start_rgb[0] + (float(end_rgb[0] - start_rgb[0]) / img.height) * y)
        g = int(start_rgb[1] + (float(end_rgb[1] - start_rgb[1]) / img.height) * y)
        b = int(start_rgb[2] + (float(end_rgb[2] - start_rgb[2]) / img.height) * y)
        draw.line([(0, y), (img.width, y)], fill=(r, g, b))

    return Image.alpha_composite(gradient, img)

def apply_background_image(qr_img: Image.Image, background_image: str) -> Image.Image:
    """
    Apply a background image to the QR code.

    Parameters:
        qr_img (Image.Image): The QR code image.
        background_image (str): Path to the background image.

    Returns:
        Image.Image: The QR code with the background image applied.
    """
    logging.info(f"Applying background image from {background_image}")
    bg = Image.open(background_image).convert("RGBA")
    bg = bg.resize(qr_img.size)
    return Image.alpha_composite(bg, qr_img)
