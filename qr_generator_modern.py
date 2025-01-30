import sys
import qrcode
from PIL import Image
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox,
                             QSlider, QColorDialog, QFrame)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QColor

class QRGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowIcon(QIcon('icon.png'))  # Add your own icon here
        
    def initUI(self):
        self.setWindowTitle('Joel Rufus')
        self.setGeometry(300, 300, 500, 450)
        self.setMinimumSize(QSize(500, 450))
        
        # Set modern style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #dddfe2;
            }
            QLabel {
                color: #1d2129;
                font-size: 14px;
            }
            QPushButton {
                background-color: #1877f2;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #166fe5;
            }
            QLineEdit {
                border: 1px solid #dddfe2;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QSlider::groove:horizontal {
                height: 4px;
                background: #e4e6eb;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #1877f2;
                border: none;
                width: 16px;
                height: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }
            .note {
                color: #606770;
                font-size: 12px;
                font-style: italic;
                margin-top: 5px;
            }
            .warning {
                color: #e74c3c;
                font-size: 12px;
                margin-top: 5px;
            }
        """)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Input Section
        input_frame = QFrame()
        input_layout = QVBoxLayout(input_frame)
        input_layout.setContentsMargins(15, 15, 15, 15)
        input_layout.setSpacing(10)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL or text...")
        input_layout.addWidget(QLabel("Data to encode:"))
        input_layout.addWidget(self.url_input)

        # Color Selection
        color_layout = QHBoxLayout()
        self.qr_color_btn = QPushButton("QR Code Color")
        self.qr_color_btn.clicked.connect(lambda: self.choose_color('qr'))
        self.bg_color_btn = QPushButton("Background Color")
        self.bg_color_btn.clicked.connect(lambda: self.choose_color('bg'))
        color_layout.addWidget(self.qr_color_btn)
        color_layout.addWidget(self.bg_color_btn)
        input_layout.addLayout(color_layout)
        
        # Color contrast warning
        color_warning = QLabel("⚠️ Use high-contrast colors for better scannability")
        color_warning.setProperty("class", "warning")
        input_layout.addWidget(color_warning)

        # Logo Selection
        logo_layout = QHBoxLayout()
        self.logo_input = QLineEdit()
        self.logo_input.setReadOnly(True)
        browse_btn = QPushButton("Browse Logo")
        browse_btn.clicked.connect(self.browse_logo)
        logo_layout.addWidget(self.logo_input)
        logo_layout.addWidget(browse_btn)
        input_layout.addWidget(QLabel("Logo (optional):"))
        input_layout.addLayout(logo_layout)

        # Transparency
        self.transparency_slider = QSlider(Qt.Horizontal)
        self.transparency_slider.setRange(0, 100)
        self.transparency_slider.setValue(70)
        transparency_note = QLabel("Recommended: 70% or lower transparency for better scanning")
        transparency_note.setProperty("class", "note")
        
        input_layout.addWidget(QLabel("Transparency:"))
        input_layout.addWidget(self.transparency_slider)
        input_layout.addWidget(transparency_note)

        layout.addWidget(input_frame)

        # Generate Section
        generate_frame = QFrame()
        generate_layout = QHBoxLayout(generate_frame)
        generate_layout.setContentsMargins(15, 15, 15, 15)
        
        self.output_input = QLineEdit()
        self.output_input.setPlaceholderText("Output file name...")
        generate_btn = QPushButton("Generate QR Code")
        generate_btn.clicked.connect(self.generate_qr)
        generate_btn.setStyleSheet("background-color: #42b72a;")
        generate_btn.setCursor(Qt.PointingHandCursor)
        
        generate_layout.addWidget(self.output_input, 70)
        generate_layout.addWidget(generate_btn, 30)
        layout.addWidget(generate_frame)

        # Status Bar
        self.status_bar = self.statusBar()
        self.status_bar.setStyleSheet("color: #606770; font-size: 12px;")

        # Initialize colors
        self.qr_color = "#000000"
        self.bg_color = "#ffffff"

    def choose_color(self, target):
        color = QColorDialog.getColor()
        if color.isValid():
            if target == 'qr':
                self.qr_color = color.name()
                self.qr_color_btn.setStyleSheet(f"background-color: {self.qr_color};")
            else:
                self.bg_color = color.name()
                self.bg_color_btn.setStyleSheet(f"background-color: {self.bg_color};")

    def browse_logo(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Logo", "", "Image Files (*.png *.jpg *.jpeg)"
        )
        if file_path:
            self.logo_input.setText(file_path)

    def generate_qr(self):
        data = self.url_input.text()
        output_file = self.output_input.text() or "qr_code.png"
        transparency = self.transparency_slider.value() / 100

        if not data:
            self.show_error("Please enter data to encode!")
            return

        # Check color contrast
        bg_lum = self.calculate_luminance(QColor(self.bg_color))
        qr_lum = self.calculate_luminance(QColor(self.qr_color))
        contrast_ratio = (max(bg_lum, qr_lum) + 0.05) / (min(bg_lum, qr_lum) + 0.05)
        
        if contrast_ratio < 3:
            reply = QMessageBox.warning(
                self, "Low Contrast",
                "Warning: Color combination may result in poor scannability!\n"
                "Recommended minimum contrast ratio: 3:1\n"
                "Current contrast ratio: {:.1f}:1\n\n"
                "Do you want to continue anyway?".format(contrast_ratio),
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return

        try:
            self.generate_qr_code(
                data, 
                self.qr_color, 
                self.bg_color, 
                self.logo_input.text(), 
                output_file, 
                transparency
            )
            self.status_bar.showMessage(f"QR code generated successfully: {output_file}", 5000)
            QMessageBox.information(self, "Success", f"QR code saved as {output_file}")
        except Exception as e:
            self.show_error(str(e))

    def calculate_luminance(self, color):
        """Calculate relative luminance for contrast ratio (WCAG 2.0 formula)"""
        r = color.red() / 255
        g = color.green() / 255
        b = color.blue() / 255
        
        rs = r / 12.92 if r <= 0.03928 else ((r + 0.055)/1.055) ** 2.4
        gs = g / 12.92 if g <= 0.03928 else ((g + 0.055)/1.055) ** 2.4
        bs = b / 12.92 if b <= 0.03928 else ((b + 0.055)/1.055) ** 2.4
        
        return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs

    def generate_qr_code(self, data, qr_color, bg_color, logo_path, output_file, transparency):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color=qr_color, back_color=bg_color).convert("RGBA")

        if logo_path:
            logo = Image.open(logo_path).convert("RGBA")
            logo = logo.resize(qr_img.size, Image.Resampling.LANCZOS)
            qr_img.putalpha(int(255 * transparency))
            blended_img = Image.alpha_composite(logo, qr_img)
        else:
            blended_img = qr_img

        border_size = 20
        final_img = Image.new("RGBA", (blended_img.width + 2*border_size, blended_img.height + 2*border_size), "white")
        final_img.paste(blended_img, (border_size, border_size), blended_img)
        final_img.save(output_file)

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)
        self.status_bar.showMessage(f"Error: {message}", 5000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRGeneratorApp()
    window.show()
    sys.exit(app.exec_())