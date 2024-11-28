import psutil
import platform
from datetime import datetime
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QProgressBar, 
                           QTableWidget, QTableWidgetItem, QTabWidget)
from PyQt5.QtCore import Qt, QTimer

class SystemInfoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # System Information
        system = platform.uname()
        sysinfo = f"""
        OS: {system.system} {system.version}
        Machine: {system.machine}
        Processor: {system.processor}
        """
        layout.addWidget(QLabel(sysinfo))

class ResourceMonitorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)  # Update every second

    def initUI(self):
        layout = QVBoxLayout(self)

        # CPU Usage
        layout.addWidget(QLabel("CPU Usage:"))
        self.cpu_bar = QProgressBar()
        layout.addWidget(self.cpu_bar)

        # Memory Usage
        layout.addWidget(QLabel("Memory Usage:"))
        self.memory_bar = QProgressBar()
        layout.addWidget(self.memory_bar)

        # Disk Usage
        layout.addWidget(QLabel("Disk Usage:"))
        self.disk_bar = QProgressBar()
        layout.addWidget(self.disk_bar)

    def update_stats(self):
        # CPU
        cpu_percent = psutil.cpu_percent()
        self.cpu_bar.setValue(int(cpu_percent))
        self.cpu_bar.setFormat(f"CPU: {cpu_percent:.1f}%")

        # Memory
        memory = psutil.virtual_memory()
        self.memory_bar.setValue(int(memory.percent))
        self.memory_bar.setFormat(f"Memory: {memory.percent:.1f}%")

        # Disk
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        self.disk_bar.setValue(int(disk_percent))
        self.disk_bar.setFormat(f"Disk: {disk_percent:.1f}%")

class ProcessMonitorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_processes)
        self.timer.start(5000)  # Update every 5 seconds

    def initUI(self):
        layout = QVBoxLayout(self)

        # Process Table
        self.process_table = QTableWidget()
        self.process_table.setColumnCount(5)
        self.process_table.setHorizontalHeaderLabels([
            "PID", "Name", "CPU %", "Memory %", "Status"
        ])
        layout.addWidget(self.process_table)

    def update_processes(self):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            try:
                pinfo = proc.info
                processes.append(pinfo)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        # Sort by CPU usage
        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        
        # Update table
        self.process_table.setRowCount(min(len(processes), 10))  # Show top 10 processes
        for i, proc in enumerate(processes[:10]):
            self.process_table.setItem(i, 0, QTableWidgetItem(str(proc['pid'])))
            self.process_table.setItem(i, 1, QTableWidgetItem(proc['name']))
            self.process_table.setItem(i, 2, QTableWidgetItem(f"{proc['cpu_percent']:.1f}%"))
            self.process_table.setItem(i, 3, QTableWidgetItem(f"{proc['memory_percent']:.1f}%"))
            self.process_table.setItem(i, 4, QTableWidgetItem(proc['status']))

class DeviceMonitoringWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Create tab widget
        tabs = QTabWidget()
        
        # Add system info tab
        tabs.addTab(SystemInfoWidget(), "System Info")
        
        # Add resource monitor tab
        tabs.addTab(ResourceMonitorWidget(), "Resources")
        
        # Add process monitor tab
        tabs.addTab(ProcessMonitorWidget(), "Processes")

        layout.addWidget(tabs)

    def closeEvent(self, event):
        # Clean up any resources
        super().closeEvent(event)
