import requests
import socket
import whois
import dns.resolver
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QLineEdit, QTextEdit, QTabWidget,
                           QComboBox, QProgressBar)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import json
import os
from datetime import datetime

class OSINTWorker(QThread):
    finished = pyqtSignal(dict)
    progress = pyqtSignal(int)
    error = pyqtSignal(str)

    def __init__(self, target, scan_type):
        super().__init__()
        self.target = target
        self.scan_type = scan_type

    def run(self):
        try:
            results = {}
            if self.scan_type == "Domain Info":
                results = self.domain_info()
            elif self.scan_type == "DNS Records":
                results = self.dns_records()
            elif self.scan_type == "Port Scan":
                results = self.port_scan()
            elif self.scan_type == "Email Info":
                results = self.email_info()
            
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))

    def domain_info(self):
        self.progress.emit(20)
        try:
            w = whois.whois(self.target)
            self.progress.emit(100)
            return {
                "registrar": str(w.registrar),
                "creation_date": str(w.creation_date),
                "expiration_date": str(w.expiration_date),
                "name_servers": w.name_servers,
                "status": w.status,
                "emails": w.emails
            }
        except Exception as e:
            raise Exception(f"Error getting domain info: {str(e)}")

    def dns_records(self):
        records = {}
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT']
        progress_step = 100 // len(record_types)
        
        for i, record_type in enumerate(record_types):
            try:
                answers = dns.resolver.resolve(self.target, record_type)
                records[record_type] = [str(rdata) for rdata in answers]
            except Exception as e:
                records[record_type] = [f"Error: {str(e)}"]
            self.progress.emit((i + 1) * progress_step)
        
        return records

    def port_scan(self):
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 465, 587, 993, 995, 3306, 3389, 5432, 8080]
        results = {}
        progress_step = 100 // len(common_ports)

        try:
            ip = socket.gethostbyname(self.target)
            for i, port in enumerate(common_ports):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ip, port))
                results[port] = "Open" if result == 0 else "Closed"
                sock.close()
                self.progress.emit((i + 1) * progress_step)
        except Exception as e:
            raise Exception(f"Error during port scan: {str(e)}")

        return results

    def email_info(self):
        # Note: This is a placeholder for email OSINT capabilities
        # In a real implementation, you would want to use appropriate APIs
        # and follow legal and ethical guidelines
        return {
            "message": "Email OSINT functionality requires additional APIs and careful consideration of privacy and legal implications."
        }

class OSINTWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.scan_history = []
        self.load_history()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Create tabs
        tabs = QTabWidget()
        tabs.addTab(self.create_scanner_tab(), "Scanner")
        tabs.addTab(self.create_history_tab(), "History")
        layout.addWidget(tabs)

    def create_scanner_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Input section
        input_layout = QHBoxLayout()
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Enter domain, IP, or email...")
        input_layout.addWidget(self.target_input)

        self.scan_type_combo = QComboBox()
        self.scan_type_combo.addItems([
            "Domain Info",
            "DNS Records",
            "Port Scan",
            "Email Info"
        ])
        input_layout.addWidget(self.scan_type_combo)

        self.scan_button = QPushButton("Start Scan")
        self.scan_button.clicked.connect(self.start_scan)
        input_layout.addWidget(self.scan_button)
        layout.addLayout(input_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # Results display
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        layout.addWidget(self.results_display)

        return widget

    def create_history_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.history_display = QTextEdit()
        self.history_display.setReadOnly(True)
        layout.addWidget(self.history_display)
        self.update_history_display()

        return widget

    def start_scan(self):
        target = self.target_input.text().strip()
        if not target:
            return

        self.scan_button.setEnabled(False)
        self.progress_bar.setValue(0)
        self.results_display.clear()
        self.results_display.append(f"Starting scan for: {target}\n")

        # Add to history
        self.add_to_history(target)

        # Create and start OSINT worker
        self.osint_worker = OSINTWorker(target, self.scan_type_combo.currentText())
        self.osint_worker.finished.connect(self.handle_results)
        self.osint_worker.progress.connect(self.progress_bar.setValue)
        self.osint_worker.error.connect(self.handle_error)
        self.osint_worker.start()

    def handle_results(self, results):
        self.results_display.clear()
        self.results_display.append("Scan Results:\n")
        self.results_display.append(json.dumps(results, indent=2))
        self.scan_button.setEnabled(True)

    def handle_error(self, error_message):
        self.results_display.append(f"\nError: {error_message}")
        self.scan_button.setEnabled(True)
        self.progress_bar.setValue(0)

    def add_to_history(self, target):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.scan_history.append({
            'target': target,
            'timestamp': timestamp,
            'type': self.scan_type_combo.currentText()
        })
        self.save_history()
        self.update_history_display()

    def update_history_display(self):
        self.history_display.clear()
        for item in reversed(self.scan_history[-10:]):  # Show last 10 scans
            self.history_display.append(
                f"[{item['timestamp']}] {item['type']}: {item['target']}"
            )

    def save_history(self):
        history_file = os.path.join(os.path.expanduser("~"), "osint_history.json")
        with open(history_file, 'w') as f:
            json.dump(self.scan_history[-100:], f)  # Keep last 100 scans

    def load_history(self):
        history_file = os.path.join(os.path.expanduser("~"), "osint_history.json")
        try:
            with open(history_file, 'r') as f:
                self.scan_history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.scan_history = []

    def closeEvent(self, event):
        self.save_history()
        super().closeEvent(event)
