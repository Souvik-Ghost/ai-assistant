import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                           QLabel, QSizeGrip, QStackedWidget)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter

# Import feature modules
from ai_assistant.modules.visual_detection import VisualDetectionWidget
from ai_assistant.modules.audio_detection import AudioDetectionWidget
from ai_assistant.modules.device_monitoring import DeviceMonitoringWidget
from ai_assistant.modules.internet_search import InternetSearchWidget
from ai_assistant.modules.osint_tools import OSINTWidget

class FloatingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.oldPos = None
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # Create content widget with background
        content = QWidget()
        content.setObjectName("contentWidget")
        content_layout = QVBoxLayout(content)

        # Add title
        title = QLabel("AI Assistant")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        content_layout.addWidget(title)

        # Create stacked widget for different features
        self.stack = QStackedWidget()
        self.stack.addWidget(VisualDetectionWidget())
        self.stack.addWidget(AudioDetectionWidget())
        self.stack.addWidget(DeviceMonitoringWidget())
        self.stack.addWidget(InternetSearchWidget())
        self.stack.addWidget(OSINTWidget())
        content_layout.addWidget(self.stack)

        # Add feature buttons
        features = [
            "Visual Detection",
            "Audio Detection",
            "Device Monitoring",
            "Internet Search",
            "OSINT Tools"
        ]

        for i, feature in enumerate(features):
            button = QPushButton(feature)
            button.setStyleSheet("""
                QPushButton {
                    padding: 12px;
                    font-size: 16px;
                    background-color: rgba(76, 175, 80, 180);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    margin: 5px;
                }
                QPushButton:hover {
                    background-color: rgba(69, 160, 73, 200);
                }
            """)
            button.clicked.connect(lambda checked, index=i: self.stack.setCurrentIndex(index))
            content_layout.addWidget(button)

        # Add close button
        close_btn = QPushButton("×")
        close_btn.setFixedSize(30, 30)
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0);
                color: white;
                font-size: 20px;
                border: none;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 150);
            }
        """)
        content_layout.insertWidget(0, close_btn, 0, Qt.AlignRight)

        # Add size grip
        size_grip = QSizeGrip(self)
        size_grip.setStyleSheet("background: transparent;")
        content_layout.addWidget(size_grip, 0, Qt.AlignBottom | Qt.AlignRight)

        layout.addWidget(content)

        # Set style for the main content widget
        content.setStyleSheet("""
            QWidget#contentWidget {
                background-color: rgba(45, 45, 45, 180);
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 50);
            }
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.oldPos:
            delta = event.globalPos() - self.oldPos
            self.move(self.pos() + delta)
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.oldPos = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

def main():
    app = QApplication(sys.argv)
    window = FloatingWindow()
    window.show()
    sys.exit(app.exec_())
