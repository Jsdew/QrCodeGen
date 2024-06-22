# QR Code Generator

## Overview

The QR Code Generator is a robust, modular, and customizable Python tool for generating QR codes from URLs. It offers extensive customization options including logos, gradients, and background images. The tool follows best practices in coding principles to ensure security, scalability, and maintainability.

## Features

- **Generate QR Codes**: Create QR codes from URLs with customizable appearance.
- **Embed Logos**: Add logos to the center of QR codes with optional padding and shapes.
- **Apply Gradients**: Apply linear gradients to QR codes.
- **Background Images**: Overlay QR codes on background images.
- **Configuration**: Use a YAML configuration file for easy customization.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Customization](#customization)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/qr-code-generator.git
    cd qr-code-generator
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python3 -m venv qrgen_env
    source qrgen_env/bin/activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Configure settings**: Edit the `config/settings.yaml` file to specify your desired settings (see [Configuration](#configuration) for details).

2. **Run the QR code generator**:
    ```bash
    python main.py
    ```

3. **Generated QR codes**: The QR code images will be saved to the specified output paths in the configuration file.

## Configuration

The `config/settings.yaml` file controls the QR code generation parameters. Below is the updated configuration example:

```yaml
# Configuration for QR Code Generator
# Define the settings for QR code creation, output, appearance, and advanced options.

data:
  url: 'https://example.com'    # URL to encode in the QR code

output:
  qr_code_path: './files/output/custom_qr.png' # Path to save the generated QR code
  logo_path: './files/input/logo.webp'        # Path to the logo file to embed in the QR code
  final_path: './files/output_logo/qr_with_logo.png' # Path to save the final QR code with the logo
  output_format: 'PNG'          # Output format for the QR code image (e.g., PNG, JPEG)

appearance:
  fill_color: 'black'           # Foreground color of the QR code
  back_color: 'white'           # Background color of the QR code
  logo_size_ratio: 5            # Ratio to determine the size of the logo in the QR code
  padding: 10                   # Padding around the logo within the QR code
  border_color: null            # Optional border color distinct from the background
  foreground_pattern: 'squares' # Pattern for QR code modules (squares, dots)
  gradient:                     # Gradient settings (optional)
    enabled: false              # Enable or disable gradient
    start_color: 'black'        # Starting color for the gradient
    end_color: 'grey'           # Ending color for the gradient

# Advanced QR Code settings
qr_code:
  version: 1                    # QR Code version (1 to 40)
  error_correction: 'H'         # Error correction level (L, M, Q, H)
  box_size: 10                  # Size of each QR box (px)
  border: 4                     # Size of QR code border (boxes)
  width: 300                    # Width of the QR code image (px)
  height: 300                   # Height of the QR code image (px)
  quiet_zone: 4                 # Minimum quiet zone width (modules)
  background_image: null        # Path to an image to use as the background (optional)
  scale: 1.0                    # Scaling factor for the entire QR code

logo:
  shape: 'circle'               # Shape of the logo area (circle, square)

  ## Configuration Sections

* **data**: URL to encode in the QR code.
* **output**: Paths for saving the generated QR code and logo-embedded QR code.
* **appearance**: Visual aspects of the QR code, such as colors, logo size, padding, border color, and patterns.
* **qr_code**: Advanced settings for QR code generation including version, error correction, box size, border, image dimensions, quiet zone, and scaling.
* **logo**: Configuration for the logo shape (e.g., circle, square).

## Customization

* **Colors**: Adjust `fill_color` and `back_color` in the configuration.
* **Logos**: Specify `logo_path` and adjust `logo_size_ratio`, `padding`, and `shape`.
* **Gradients**: Enable and configure gradients with `gradient.enabled`, `gradient.start_color`, and `gradient.end_color`.
* **Backgrounds**: Use `background_image` to overlay the QR code on a background image.

## Testing

Unit tests are provided to ensure the robustness of the QR code generator. To run the tests:

Run all tests:
```bash
python -m unittest discover tests

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Push to your branch and create a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.