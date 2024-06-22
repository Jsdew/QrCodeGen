# tests/test_utils.py
import unittest
from src.utils import validate_url, ensure_directory_exists, sanitize_file_path, validate_color, validate_configuration
import os
import tempfile

class TestUtils(unittest.TestCase):

    def test_validate_url(self):
        valid_urls = ['http://example.com', 'https://example.com']
        invalid_urls = ['ftp://example.com', 'example.com', 'http:/example.com']

        for url in valid_urls:
            validate_url(url)  # Should not raise an exception

        for url in invalid_urls:
            with self.assertRaises(ValueError):
                validate_url(url)

    def test_ensure_directory_exists(self):
        temp_dir = tempfile.mkdtemp()
        test_dir = os.path.join(temp_dir, 'test_directory')
        ensure_directory_exists(test_dir)
        self.assertTrue(os.path.exists(test_dir))
        os.rmdir(test_dir)  # Cleanup

    def test_sanitize_file_path(self):
        test_path = './test/../test/./path//file.txt'
        sanitized_path = sanitize_file_path(test_path)
        self.assertEqual(sanitized_path, os.path.normpath(test_path))

    def test_validate_color(self):
        valid_colors = ['#000', '#000000', '#FFFFFF']
        invalid_colors = ['#GGG', '000000', '#12345', '']

        for color in valid_colors:
            self.assertTrue(validate_color(color))

        for color in invalid_colors:
            self.assertFalse(validate_color(color))

    def test_validate_configuration(self):
        valid_config = {
            'data': {'url': 'https://example.com'},
            'output': {'qr_code_path': 'qr.png', 'logo_path': 'logo.png', 'final_path': 'final.png'},
            'appearance': {'fill_color': 'black', 'back_color': 'white', 'logo_size_ratio': 5, 'padding': 10, 'gradient': {'enabled': False}},
            'qr_code': {'version': 1, 'error_correction': 'H', 'box_size': 10, 'border': 4, 'width': 300, 'height': 300, 'quiet_zone': 4, 'scale': 1.0}
        }
        validate_configuration(valid_config)  # Should not raise an exception

        invalid_config = {
            'data': {},
            'output': {'qr_code_path': 'qr.png', 'logo_path': 'logo.png', 'final_path': 'final.png'},
            'appearance': {'fill_color': 'black', 'back_color': 'white'},
            'qr_code': {'version': 1, 'error_correction': 'H'}
        }
        with self.assertRaises(ValueError):
            validate_configuration(invalid_config)

if __name__ == '__main__':
    unittest.main()
