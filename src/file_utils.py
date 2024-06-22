# src/file_utils.py
import os
import logging
from PIL import Image

def ensure_directory_exists(directory: str) -> None:
    """
    Ensure the specified directory exists. Create it if it does not.

    Parameters:
        directory (str): The directory path to check.
    """
    if not os.path.exists(directory):
        logging.info(f"Creating directory: {directory}")
        os.makedirs(directory, exist_ok=True)

def save_image(img: Image.Image, file_path: str) -> None:
    """
    Save the image to the specified file path.

    Parameters:
        img (Image.Image): The image to save.
        file_path (str): The file path to save the image to.
    """
    ensure_directory_exists(os.path.dirname(file_path))
    img.save(file_path)
    logging.info(f"Image saved to: {file_path}")
