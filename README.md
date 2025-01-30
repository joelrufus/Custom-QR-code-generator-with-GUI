
# QR Code Generator

A modern and customizable QR Code Generator with a PyQt5-based GUI. This application allows you to generate QR codes with custom colors, logos, and transparency settings.


## Features
- 🎨 **Custom QR Code Colors**: Choose any color for the QR code and background.
- 🏷️ **Logo Embedding**: Add a logo to the center of the QR code.
- 🔍 **Transparency Control**: Adjust the transparency of the QR code over the logo.
- ⚠️ **High-Contrast Warnings**: Get warnings if the color combination might make the QR code unscannable.
- 📦 **Executable Build**: Easily create a standalone executable for Windows, macOS, or Linux.

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/joelrufus/Custom-QR-code-generator-with-GUI.git
   cd Custom-QR-code-generator-with-GUI
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python qr_generator_modern.py
   ```

## Usage
1. Enter the data you want to encode (e.g., a URL or text).
2. Customize the QR code colors and transparency.
3. Optionally, add a logo to the center of the QR code.
4. Click "Generate QR Code" to create and save the QR code.

## Building the Executable
To create a standalone executable:
1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Build the executable:
   ```bash
   pyinstaller --onefile --windowed qr_generator_modern.py
   ```

3. The executable will be located in the `dist/` folder.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request.


## Acknowledgments
- Built with [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) for the GUI.
- QR Code generation powered by [qrcode](https://github.com/lincolnloop/python-qrcode).
- Inspired by modern UI design principles.

---

Made with ❤️ by [Joel Rufus](https://github.com/joelrufus)
```

