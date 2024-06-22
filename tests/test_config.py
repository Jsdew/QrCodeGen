# tests/test_config.py
import unittest
from src.config import load_config
import tempfile
import os
import yaml

class TestConfig(unittest.TestCase):

    def test_load_config(self):
        config_data = {
            'data': {'url': 'https://example.com'},
            'output': {'qr_code_path': 'qr.png', 'logo_path': 'logo.png', 'final_path': 'final.png'},
            'appearance': {'fill_color': 'black', 'back_color': 'white', 'logo_size_ratio': 5, 'padding': 10},
            'qr_code': {'version': 1, 'error_correction': 'H', 'box_size': 10, 'border': 4, 'width': 300, 'height': 300, 'quiet_zone': 4, 'scale': 1.0}
        }
        with tempfile.NamedTemporaryFile(delete=False, suffix='.yaml', mode='w') as tmpfile:
            yaml.dump(config_data, tmpfile)
            tmpfile_path = tmpfile.name

        loaded_config = load_config(tmpfile_path)
        self.assertEqual(loaded_config, config_data)
        os.remove(tmpfile_path)  # Cleanup

if __name__ == '__main__':
    unittest.main()
