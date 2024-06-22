"""
This module initializes the src package, making key functions available for easy import.

Public API:
- generate_qr_code
- apply_gradient
- apply_background_image
- add_logo_to_qr
- save_image
- ensure_directory_exists
- load_config
- validate_url
- validate_configuration
- configure_logging
- log_execution_time
"""

from src.qr_generator import generate_qr_code
from src.image_utils import apply_gradient, apply_background_image
from src.logo_embedder import add_logo_to_qr
from src.file_utils import save_image, ensure_directory_exists
from src.config import load_config
from src.utils import validate_url, validate_configuration
from src.logger import configure_logging, log_execution_time

__all__ = [
    'generate_qr_code',
    'apply_gradient',
    'apply_background_image',
    'add_logo_to_qr',
    'save_image',
    'ensure_directory_exists',
    'load_config',
    'validate_url',
    'validate_configuration',
    'configure_logging',
    'log_execution_time'
]

# Ensure the module works even if a specific import fails
try:
    from src.qr_generator import generate_qr_code
except ImportError as e:
    print(f"Warning: {e}. QR code generation might not be available.")

try:
    from src.image_utils import apply_gradient, apply_background_image
except ImportError as e:
    print(f"Warning: {e}. Image utilities might not be available.")

try:
    from src.logo_embedder import add_logo_to_qr
except ImportError as e:
    print(f"Warning: {e}. Logo embedding might not be available.")

try:
    from src.file_utils import save_image, ensure_directory_exists
except ImportError as e:
    print(f"Warning: {e}. File utilities might not be available.")

try:
    from src.config import load_config
except ImportError as e:
    print(f"Warning: {e}. Configuration loading might not be available.")

try:
    from src.utils import validate_url, validate_configuration
except ImportError as e:
    print(f"Warning: {e}. URL validation or configuration validation might not be available.")

try:
    from src.logger import configure_logging, log_execution_time
except ImportError as e:
    print(f"Warning: {e}. Logging setup and execution time tracking might not be available.")
