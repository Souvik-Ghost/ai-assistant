# Installation Guide

## Windows Installation

### Prerequisites
- Python 3.8 or higher
- Git (optional)
- Windows 10 or higher

### Steps
1. **Download the Project**
   ```bash
   git clone https://github.com/Souvik-Ghost/ai_assistant.git
   cd ai_assistant
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python -m ai_assistant
   ```

### Using the Windows Installer
1. Download the latest release from [Releases](https://github.com/Souvik-Ghost/ai_assistant/releases)
2. Run the installer
3. Follow the installation wizard

## Android Installation

### Prerequisites
- Termux
- Python 3.8+
- VNC Viewer

### Steps
1. **Install Required Packages**
   ```bash
   pkg update && pkg upgrade
   pkg install python git x11-repo
   pkg install tigervnc
   ```

2. **Clone and Setup**
   ```bash
   cd storage/shared
   git clone https://github.com/Souvik-Ghost/ai_assistant.git
   cd ai_assistant
   ```

3. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Start VNC Server**
   ```bash
   vncserver
   ```

6. **Run the Application**
   ```bash
   python -m ai_assistant
   ```

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Permission Issues**
   - Run as administrator (Windows)
   - Check Termux permissions (Android)

3. **Graphics Issues**
   - Update graphics drivers
   - Check VNC configuration

### Getting Help
- Open an [issue](https://github.com/Souvik-Ghost/ai_assistant/issues)
- Check [Discussions](https://github.com/Souvik-Ghost/ai_assistant/discussions)
- Review error logs in `logs/` directory
