import numpy as np
import sounddevice as sd
import queue
import threading
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                           QProgressBar, QComboBox)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal

class AudioDetectionWidget(QWidget):
    audio_level_update = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.audio_queue = queue.Queue()
        self.stream = None
        self.is_recording = False
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Device selection
        self.device_combo = QComboBox()
        self.update_devices()
        layout.addWidget(QLabel("Audio Device:"))
        layout.addWidget(self.device_combo)

        # Volume meter
        self.level_bar = QProgressBar()
        self.level_bar.setMinimum(0)
        self.level_bar.setMaximum(100)
        self.level_bar.setTextVisible(True)
        self.level_bar.setFormat("Volume: %p%")
        layout.addWidget(self.level_bar)

        # Audio detection status
        self.status_label = QLabel("Status: Ready")
        layout.addWidget(self.status_label)

        # Control buttons
        self.start_button = QPushButton("Start Audio Detection")
        self.start_button.clicked.connect(self.toggle_audio)
        layout.addWidget(self.start_button)

        # Connect signal to update UI
        self.audio_level_update.connect(self.update_level_bar)

        # Update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.process_audio_queue)
        self.update_timer.start(50)  # 50ms update interval

    def update_devices(self):
        self.device_combo.clear()
        devices = sd.query_devices()
        for i, dev in enumerate(devices):
            if dev['max_input_channels'] > 0:
                self.device_combo.addItem(f"{dev['name']}", i)

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(f"Audio callback status: {status}")
        volume_norm = np.linalg.norm(indata) * 10
        self.audio_queue.put(volume_norm)

    def process_audio_queue(self):
        try:
            while True:
                volume = self.audio_queue.get_nowait()
                self.audio_level_update.emit(volume)
        except queue.Empty:
            pass

    def update_level_bar(self, value):
        # Scale the value to 0-100 range
        scaled_value = min(100, int(value * 5))
        self.level_bar.setValue(scaled_value)
        
        # Update status based on volume
        if scaled_value > 80:
            self.status_label.setText("Status: Loud Sound Detected!")
            self.status_label.setStyleSheet("color: red;")
        elif scaled_value > 50:
            self.status_label.setText("Status: Normal Speech Level")
            self.status_label.setStyleSheet("color: green;")
        else:
            self.status_label.setText("Status: Quiet")
            self.status_label.setStyleSheet("color: black;")

    def toggle_audio(self):
        if self.is_recording:
            self.stop_audio()
        else:
            self.start_audio()

    def start_audio(self):
        try:
            device_idx = self.device_combo.currentData()
            self.stream = sd.InputStream(
                device=device_idx,
                channels=1,
                callback=self.audio_callback,
                blocksize=1024,
                samplerate=44100
            )
            self.stream.start()
            self.is_recording = True
            self.start_button.setText("Stop Audio Detection")
            self.status_label.setText("Status: Listening...")
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")

    def stop_audio(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        self.is_recording = False
        self.start_button.setText("Start Audio Detection")
        self.status_label.setText("Status: Ready")
        self.level_bar.setValue(0)

    def closeEvent(self, event):
        self.stop_audio()
        super().closeEvent(event)
