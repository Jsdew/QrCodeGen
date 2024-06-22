# tests/test_qr_code.py
import unittest
from src.qr_generator import generate_qr_code
from src.image_utils import apply_gradient, apply_background_image
from src.logo_embedder import add_logo_to_qr
from src.file_utils import ensure_directory_exists, save_image
from PIL import Image
import os

class TestQRCodeGeneration(unittest.TestCase):

    def setUp(self):
        self.data = 'https://example.com'
        self.file_path = 'tests/test_qr.png'
        self.logo_path = 'tests/test_logo.png'
        self.output_path = 'tests/test_qr_with_logo.png'
        self.bg_image_path = 'tests/test_bg.png'
        
        # Create test logo and background images
        logo = Image.new('RGBA', (50, 50), (255, 0, 0, 255))
        logo.save(self.logo_path)
        bg = Image.new('RGBA', (300, 300), (0, 255, 0, 255))
        bg.save(self.bg_image_path)

    def tearDown(self):
        # Remove test files
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        if os.path.exists(self.logo_path):
            os.remove(self.logo_path)
        if os.path.exists(self.output_path):
            os.remove(self.output_path)
        if os.path.exists(self.bg_image_path):
            os.remove(self.bg_image_path)

    def test_generate_qr_code(self):
        img = generate_qr_code(self.data, fill_color='black', back_color='white')
        self.assertIsInstance(img, Image.Image)
        save_image(img, self.file_path)
        self.assertTrue(os.path.exists(self.file_path))

    def test_apply_gradient(self):
        img = generate_qr_code(self.data)
        gradient_img = apply_gradient(img, '#000000', '#FFFFFF')
        self.assertIsInstance(gradient_img, Image.Image)

    def test_apply_background_image(self):
        img = generate_qr_code(self.data)
        img_with_bg = apply_background_image(img, self.bg_image_path)
        self.assertIsInstance(img_with_bg, Image.Image)

    def test_add_logo_to_qr(self):
        img = generate_qr_code(self.data)
        add_logo_to_qr(img, self.logo_path, self.output_path)
        self.assertTrue(os.path.exists(self.output_path))

if __name__ == '__main__':
    unittest.main()
